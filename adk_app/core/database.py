"""
Snowflake Database Connection Manager.
Handles connection lifecycle, pooling, and error handling.
"""
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import snowflake.connector
from snowflake.connector import SnowflakeConnection, DictCursor

logger = logging.getLogger(__name__)


class SnowflakeConnectionManager:
    """
    Manages Snowflake database connections with proper lifecycle management.
    Implements connection pooling and automatic cleanup.
    """
    
    def __init__(self):
        self._connection: Optional[SnowflakeConnection] = None
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load Snowflake configuration from environment and settings."""
        # Get PEM file path from environment variable
        pem_file_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_FILE")
        
        if not pem_file_path:
            # Fallback to default location if not set
            base_dir = Path(__file__).parent.parent.parent
            pem_file_path = str(base_dir / "database_connection_config.pem")
            logger.warning(
                f"SNOWFLAKE_PRIVATE_KEY_FILE not set in .env, using default: {pem_file_path}"
            )
        else:
            # Resolve path (handles ~, relative paths, etc.)
            pem_file_path = os.path.expanduser(pem_file_path)
            
            # If relative path, make it relative to project root
            if not os.path.isabs(pem_file_path):
                base_dir = Path(__file__).parent.parent.parent
                pem_file_path = str(base_dir / pem_file_path)
        
        config = {
            "user": os.getenv("SNOWFLAKE_USER", "ML_SRV_USER"),
            "account": os.getenv("SNOWFLAKE_ACCOUNT", "ae18467.eu-west-2.aws"),
            "role": os.getenv("SNOWFLAKE_ROLE", "ML_SRV_RO_ROLE"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "DEV_DATA_ML_WH"),
            "database": os.getenv("SNOWFLAKE_DATABASE", "DEV_DATA_ML_DB"),
            "schema": os.getenv("SNOWFLAKE_SCHEMA", "DATA_ML_SCHEMA"),
            "private_key_file": pem_file_path
        }
        
        logger.info(f"Using PEM file: {pem_file_path}")
        
        return config
    
    def connect(self) -> SnowflakeConnection:
        """
        Establish connection to Snowflake.
        
        Returns:
            Active Snowflake connection
            
        Raises:
            snowflake.connector.Error: If connection fails
        """
        if self._connection is not None and not self._connection.is_closed():
            return self._connection
        
        try:
            logger.info(f"Connecting to Snowflake account: {self._config['account']}")
            
            # Check if PEM file exists
            pem_file = Path(self._config["private_key_file"])
            if not pem_file.exists():
                raise FileNotFoundError(
                    f"Private key file not found: {pem_file}. "
                    "Please ensure database_connection_config.pem is in the project root."
                )
            
            self._connection = snowflake.connector.connect(
                user=self._config["user"],
                private_key_file=self._config["private_key_file"],
                account=self._config["account"],
                role=self._config["role"],
                warehouse=self._config["warehouse"],
                database=self._config["database"],
                schema=self._config["schema"]
            )
            
            logger.info("Successfully connected to Snowflake")
            return self._connection
            
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            raise
    
    def close(self):
        """Close the Snowflake connection."""
        if self._connection is not None and not self._connection.is_closed():
            try:
                self._connection.close()
                logger.info("Snowflake connection closed")
            except Exception as e:
                logger.error(f"Error closing Snowflake connection: {str(e)}")
            finally:
                self._connection = None
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for Snowflake connections.
        Automatically handles connection lifecycle.
        
        Usage:
            with manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        conn = None
        try:
            conn = self.connect()
            yield conn
        except Exception as e:
            logger.error(f"Error in connection context: {str(e)}")
            raise
        finally:
            if conn is not None:
                # Don't close here, let the manager handle it
                pass
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[Dict[str, Any]] = None,
        fetch_all: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Execute a query and return results as list of dictionaries.
        
        Args:
            query: SQL query to execute
            params: Optional query parameters
            fetch_all: If True, fetch all results; if False, fetch one
            
        Returns:
            List of dictionaries with query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(DictCursor)
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if fetch_all:
                    results = cursor.fetchall()
                else:
                    result = cursor.fetchone()
                    results = [result] if result else []
                
                return results
                
            except Exception as e:
                logger.error(f"Query execution failed: {str(e)}")
                logger.error(f"Query: {query}")
                raise
            finally:
                cursor.close()
    
    def test_connection(self) -> bool:
        """
        Test the Snowflake connection.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT CURRENT_VERSION()")
                version = cursor.fetchone()
                cursor.close()
                logger.info(f"Snowflake connection test successful. Version: {version[0]}")
                return True
        except Exception as e:
            logger.error(f"Snowflake connection test failed: {str(e)}")
            return False
    
    def __enter__(self):
        """Support for context manager protocol."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager protocol."""
        self.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()


# Global connection manager instance
_connection_manager: Optional[SnowflakeConnectionManager] = None


def get_snowflake_manager() -> SnowflakeConnectionManager:
    """
    Get or create the global Snowflake connection manager.
    
    Returns:
        SnowflakeConnectionManager instance
    """
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = SnowflakeConnectionManager()
    return _connection_manager


def close_snowflake_connections():
    """Close all Snowflake connections."""
    global _connection_manager
    if _connection_manager is not None:
        _connection_manager.close()
        _connection_manager = None
