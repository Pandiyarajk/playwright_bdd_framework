"""JSON data provider."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from framework.data_providers.base_provider import BaseDataProvider


class JsonProvider(BaseDataProvider):
    """Provider for JSON data sources."""
    
    def __init__(self, source: str):
        """
        Initialize JSON provider.
        
        Args:
            source: Path to JSON file
        """
        super().__init__(source)
        self.file_path = Path(source)
        self.data = None
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {source}")
        
        self._load_data()
    
    def _load_data(self) -> None:
        """Load JSON data from file."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def get_data(self, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get data from JSON file.
        
        Args:
            key: Dot-notation key path (e.g., 'user.address.city')
            default: Default value if key not found
            
        Returns:
            Data at the specified key or entire data if key is None
        """
        if key is None:
            return self.data
        
        # Support dot notation for nested keys
        keys = key.split('.')
        value = self.data
        
        try:
            for k in keys:
                # Support array indexing
                if '[' in k and ']' in k:
                    key_name = k[:k.index('[')]
                    index = int(k[k.index('[') + 1:k.index(']')])
                    value = value[key_name][index]
                else:
                    value = value[k]
            return value
        except (KeyError, IndexError, TypeError):
            return default
    
    def get_all_data(self) -> List[Dict[str, Any]]:
        """
        Get all data from JSON file.
        
        Returns:
            List of data records (if root is list) or single item list
        """
        if isinstance(self.data, list):
            return self.data
        return [self.data]
    
    def get_by_filter(self, filter_func: callable) -> List[Dict[str, Any]]:
        """
        Filter data using a custom function.
        
        Args:
            filter_func: Function that takes a data item and returns bool
            
        Returns:
            Filtered list of data items
        """
        all_data = self.get_all_data()
        return [item for item in all_data if filter_func(item)]
    
    def get_by_key_value(self, key: str, value: Any) -> Optional[Dict[str, Any]]:
        """
        Find first item matching key-value pair.
        
        Args:
            key: Key to search for
            value: Value to match
            
        Returns:
            First matching item or None
        """
        all_data = self.get_all_data()
        for item in all_data:
            if isinstance(item, dict) and item.get(key) == value:
                return item
        return None
    
    def reload(self) -> None:
        """Reload data from file."""
        self._load_data()