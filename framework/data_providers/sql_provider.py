"""SQL database data providers (MS SQL Server, SQLite)."""

import sqlite3
from typing import Any, Dict, List, Optional, Tuple
from framework.data_providers.base_provider import BaseDataProvider

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

try:
    import pymssql
    PYMSSQL_AVAILABLE = True
except ImportError:
    PYMSSQL_AVAILABLE = False


class SqlServerProvider(BaseDataProvider):
    """Provider for MS SQL Server data source."""
    
    def __init__(
        self,
        source: str = None,
        server: str = None,
        database: str = None,
        username: str = None,
        password: str = None,
        driver: str = "ODBC Driver 17 for SQL Server",
        use_pymssql: bool = False
    ):
        """
        Initialize SQL Server provider.
        
        Args:
            source: Connection string (if provided, other params ignored)
            server: Server address
            database: Database name
            username: Username
            password: Password
            driver: ODBC driver name
            use_pymssql: Use pymssql instead of pyodbc
        """
        super().__init__(source or "")
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.use_pymssql = use_pymssql
        self.connection = None
        self.cursor = None
        
        if not source:
            if not all([server, database, username, password]):
                raise ValueError("Must provide either connection string or all connection parameters")
            
            if use_pymssql:
                if not PYMSSQL_AVAILABLE:
                    raise ImportError("pymssql is not installed. Install with: pip install pymssql")
            else:
                if not PYODBC_AVAILABLE:
                    raise ImportError("pyodbc is not installed. Install with: pip install pyodbc")
        
        self._connect()
    
    def _connect(self) -> None:
        """Establish database connection."""
        try:
            if self.source:
                # Use connection string
                if self.use_pymssql:
                    raise ValueError("Connection string not supported with pymssql")
                self.connection = pyodbc.connect(self.source)
            else:
                # Build connection
                if self.use_pymssql:
                    self.connection = pymssql.connect(
                        server=self.server,
                        database=self.database,
                        user=self.username,
                        password=self.password
                    )
                else:
                    conn_str = (
                        f"DRIVER={{{self.driver}}};"
                        f"SERVER={self.server};"
                        f"DATABASE={self.database};"
                        f"UID={self.username};"
                        f"PWD={self.password}"
                    )
                    self.connection = pyodbc.connect(conn_str)
            
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQL Server: {str(e)}")
    
    def get_data(
        self,
        query: str,
        params: Optional[Tuple] = None,
        as_dict: bool = True
    ) -> Any:
        """
        Execute query and get data.
        
        Args:
            query: SQL query
            params: Query parameters
            as_dict: Return results as dictionaries
            
        Returns:
            Query results
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            rows = self.cursor.fetchall()
            
            if as_dict:
                columns = [column[0] for column in self.cursor.description]
                return [dict(zip(columns, row)) for row in rows]
            
            return rows
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")
    
    def get_all_data(self, table: str) -> List[Dict[str, Any]]:
        """
        Get all data from a table.
        
        Args:
            table: Table name
            
        Returns:
            List of dictionaries containing row data
        """
        query = f"SELECT * FROM {table}"
        return self.get_data(query, as_dict=True)
    
    def execute(self, query: str, params: Optional[Tuple] = None) -> int:
        """
        Execute a non-query SQL statement.
        
        Args:
            query: SQL statement
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Query execution failed: {str(e)}")
    
    def get_single_value(
        self,
        query: str,
        params: Optional[Tuple] = None
    ) -> Any:
        """
        Get single value from query.
        
        Args:
            query: SQL query
            params: Query parameters
            
        Returns:
            Single value
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")
    
    def close(self) -> None:
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


class SqliteProvider(BaseDataProvider):
    """Provider for SQLite data source."""
    
    def __init__(self, source: str):
        """
        Initialize SQLite provider.
        
        Args:
            source: Path to SQLite database file
        """
        super().__init__(source)
        self.connection = None
        self.cursor = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.source)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQLite database: {str(e)}")
    
    def get_data(
        self,
        query: str,
        params: Optional[Tuple] = None,
        as_dict: bool = True
    ) -> Any:
        """
        Execute query and get data.
        
        Args:
            query: SQL query
            params: Query parameters
            as_dict: Return results as dictionaries
            
        Returns:
            Query results
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            rows = self.cursor.fetchall()
            
            if as_dict:
                return [dict(row) for row in rows]
            
            return rows
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")
    
    def get_all_data(self, table: str) -> List[Dict[str, Any]]:
        """
        Get all data from a table.
        
        Args:
            table: Table name
            
        Returns:
            List of dictionaries containing row data
        """
        query = f"SELECT * FROM {table}"
        return self.get_data(query, as_dict=True)
    
    def execute(self, query: str, params: Optional[Tuple] = None) -> int:
        """
        Execute a non-query SQL statement.
        
        Args:
            query: SQL statement
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Query execution failed: {str(e)}")
    
    def get_single_value(
        self,
        query: str,
        params: Optional[Tuple] = None
    ) -> Any:
        """
        Get single value from query.
        
        Args:
            query: SQL query
            params: Query parameters
            
        Returns:
            Single value
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")
    
    def get_tables(self) -> List[str]:
        """
        Get list of all tables in database.
        
        Returns:
            List of table names
        """
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        results = self.get_data(query, as_dict=False)
        return [row[0] for row in results]
    
    def close(self) -> None:
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()