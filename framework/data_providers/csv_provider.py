"""CSV data provider."""

import csv
from pathlib import Path
from typing import Any, Dict, List, Optional
from framework.data_providers.base_provider import BaseDataProvider


class CsvProvider(BaseDataProvider):
    """Provider for CSV data sources."""
    
    def __init__(
        self,
        source: str,
        delimiter: str = ',',
        has_header: bool = True,
        encoding: str = 'utf-8'
    ):
        """
        Initialize CSV provider.
        
        Args:
            source: Path to CSV file
            delimiter: CSV delimiter (default: ',')
            has_header: Whether first row is header
            encoding: File encoding
        """
        super().__init__(source)
        self.file_path = Path(source)
        self.delimiter = delimiter
        self.has_header = has_header
        self.encoding = encoding
        self.data = []
        self.headers = []
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {source}")
        
        self._load_data()
    
    def _load_data(self) -> None:
        """Load CSV data from file."""
        with open(self.file_path, 'r', encoding=self.encoding, newline='') as f:
            if self.has_header:
                reader = csv.DictReader(f, delimiter=self.delimiter)
                self.headers = reader.fieldnames
                self.data = list(reader)
            else:
                reader = csv.reader(f, delimiter=self.delimiter)
                self.data = list(reader)
    
    def get_data(
        self,
        row: Optional[int] = None,
        column: Optional[str] = None
    ) -> Any:
        """
        Get data from CSV file.
        
        Args:
            row: Row index (0-based)
            column: Column name (if has_header) or index
            
        Returns:
            Cell value, row data, or column data
        """
        # Get specific row
        if row is not None and column is None:
            if 0 <= row < len(self.data):
                return self.data[row]
            return None
        
        # Get specific column
        if column is not None and row is None:
            if self.has_header:
                return [row.get(column) for row in self.data]
            else:
                try:
                    col_idx = int(column)
                    return [row[col_idx] for row in self.data]
                except (ValueError, IndexError):
                    return None
        
        # Get specific cell
        if row is not None and column is not None:
            if 0 <= row < len(self.data):
                if self.has_header:
                    return self.data[row].get(column)
                else:
                    try:
                        col_idx = int(column)
                        return self.data[row][col_idx]
                    except (ValueError, IndexError):
                        return None
        
        return None
    
    def get_all_data(self) -> List[Dict[str, Any]]:
        """
        Get all data from CSV file.
        
        Returns:
            List of data records
        """
        return self.data
    
    def get_by_filter(self, filter_func: callable) -> List[Dict[str, Any]]:
        """
        Filter data using a custom function.
        
        Args:
            filter_func: Function that takes a row and returns bool
            
        Returns:
            Filtered list of rows
        """
        return [row for row in self.data if filter_func(row)]
    
    def get_by_column_value(
        self,
        column: str,
        value: Any
    ) -> List[Dict[str, Any]]:
        """
        Find all rows where column matches value.
        
        Args:
            column: Column name
            value: Value to match
            
        Returns:
            List of matching rows
        """
        if not self.has_header:
            return []
        
        return [row for row in self.data if row.get(column) == value]
    
    def get_row_count(self) -> int:
        """
        Get row count.
        
        Returns:
            Number of data rows
        """
        return len(self.data)
    
    def get_column_count(self) -> int:
        """
        Get column count.
        
        Returns:
            Number of columns
        """
        if self.has_header:
            return len(self.headers)
        elif self.data:
            return len(self.data[0])
        return 0
    
    def reload(self) -> None:
        """Reload data from file."""
        self.data = []
        self.headers = []
        self._load_data()