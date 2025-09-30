"""Text file data provider."""

from pathlib import Path
from typing import Any, Dict, List, Optional
from framework.data_providers.base_provider import BaseDataProvider


class TxtProvider(BaseDataProvider):
    """Provider for text file data sources."""
    
    def __init__(
        self,
        source: str,
        encoding: str = 'utf-8',
        strip_lines: bool = True
    ):
        """
        Initialize text provider.
        
        Args:
            source: Path to text file
            encoding: File encoding
            strip_lines: Whether to strip whitespace from lines
        """
        super().__init__(source)
        self.file_path = Path(source)
        self.encoding = encoding
        self.strip_lines = strip_lines
        self.lines = []
        self.content = ""
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Text file not found: {source}")
        
        self._load_data()
    
    def _load_data(self) -> None:
        """Load text data from file."""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            self.content = f.read()
            f.seek(0)
            self.lines = f.readlines()
            
            if self.strip_lines:
                self.lines = [line.strip() for line in self.lines]
    
    def get_data(
        self,
        line: Optional[int] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None
    ) -> Any:
        """
        Get data from text file.
        
        Args:
            line: Specific line number (0-based)
            start_line: Start line for range (0-based, inclusive)
            end_line: End line for range (0-based, exclusive)
            
        Returns:
            Line content, line range, or entire content
        """
        # Get specific line
        if line is not None:
            if 0 <= line < len(self.lines):
                return self.lines[line]
            return None
        
        # Get line range
        if start_line is not None and end_line is not None:
            return self.lines[start_line:end_line]
        
        # Get all content
        return self.content
    
    def get_all_data(self) -> List[Dict[str, Any]]:
        """
        Get all data from text file.
        
        Returns:
            List of dictionaries with line numbers and content
        """
        return [
            {"line_number": i, "content": line}
            for i, line in enumerate(self.lines)
        ]
    
    def get_lines(self) -> List[str]:
        """
        Get all lines as a list.
        
        Returns:
            List of lines
        """
        return self.lines
    
    def get_content(self) -> str:
        """
        Get entire file content as string.
        
        Returns:
            Complete file content
        """
        return self.content
    
    def search(self, pattern: str, case_sensitive: bool = True) -> List[Dict[str, Any]]:
        """
        Search for pattern in text.
        
        Args:
            pattern: Search pattern
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            List of matching lines with line numbers
        """
        results = []
        search_pattern = pattern if case_sensitive else pattern.lower()
        
        for i, line in enumerate(self.lines):
            search_line = line if case_sensitive else line.lower()
            if search_pattern in search_line:
                results.append({
                    "line_number": i,
                    "content": line,
                    "position": search_line.index(search_pattern)
                })
        
        return results
    
    def get_line_count(self) -> int:
        """
        Get line count.
        
        Returns:
            Number of lines
        """
        return len(self.lines)
    
    def get_non_empty_lines(self) -> List[str]:
        """
        Get all non-empty lines.
        
        Returns:
            List of non-empty lines
        """
        return [line for line in self.lines if line]
    
    def reload(self) -> None:
        """Reload data from file."""
        self.lines = []
        self.content = ""
        self._load_data()