"""Dashboard toolset for organizing database query and analytics tools."""

from google.adk.tools import FunctionTool
from ..dashboard_tools import (
    get_database_schema,
    generate_and_execute_query,
    get_table_summary
)


class DashboardToolset:
    """Collection of dashboard and database query tools."""
    
    @staticmethod
    def get_tools():
        """Get all dashboard tools for database querying and analytics."""
        return [
            FunctionTool(func=get_database_schema),
            FunctionTool(func=generate_and_execute_query),
            FunctionTool(func=get_table_summary)
        ]
