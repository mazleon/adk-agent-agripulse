"""
Settings and configuration management.
Loads environment variables and YAML configurations.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from functools import lru_cache


class Settings:
    """Application settings loaded from environment and config files."""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Base paths
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "adk_app" / "config"
        
        # Load configurations
        self.runtime_config = self._load_yaml("runtime.yaml")
        self.models_config = self._load_yaml("models.yaml")
        
        # Environment variables
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self.environment = os.getenv("ENVIRONMENT", "development")
        
        # Set API key in environment for ADK
        if self.google_api_key:
            os.environ["GOOGLE_API_KEY"] = self.google_api_key
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a YAML configuration file."""
        file_path = self.config_dir / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def get_model_config(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get model configuration for a specific agent or default."""
        models = self.models_config.get("models", {})
        if agent_name and agent_name in models:
            return models[agent_name]
        return models.get("default", {})
    
    def get_runtime_config(self, key: str, default: Any = None) -> Any:
        """Get a runtime configuration value."""
        keys = key.split(".")
        value = self.runtime_config.get("runtime", {})
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value if value is not None else default
    
    @property
    def dev_ui_enabled(self) -> bool:
        """Check if development UI is enabled."""
        return self.get_runtime_config("dev_ui.enabled", True)
    
    @property
    def dev_ui_port(self) -> int:
        """Get development UI port."""
        return self.get_runtime_config("dev_ui.port", 8080)
    
    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get_runtime_config("logging.level", "INFO")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
