"""Base data provider interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseDataProvider(ABC):
    """Abstract base class for all data providers."""
    
    def __init__(self, source: str):
        """
        Initialize data provider.
        
        Args:
            source: Data source path or connection string
        """
        self.source = source
    
    @abstractmethod
    def get_data(self, **kwargs) -> Any:
        """
        Get data from the source.
        
        Returns:
            Data in appropriate format
        """
        pass
    
    @abstractmethod
    def get_all_data(self) -> List[Dict[str, Any]]:
        """
        Get all data from the source.
        
        Returns:
            List of data records
        """
        pass
    
    def close(self) -> None:
        """Close any open connections or resources."""
        pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()