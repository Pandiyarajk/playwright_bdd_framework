"""File utility functions."""

import os
import shutil
import json
from pathlib import Path
from typing import List, Optional


class FileUtils:
    """File manipulation utilities."""
    
    @staticmethod
    def create_directory(path: str, exist_ok: bool = True) -> None:
        """
        Create directory.
        
        Args:
            path: Directory path
            exist_ok: Don't raise error if directory exists
        """
        Path(path).mkdir(parents=True, exist_ok=exist_ok)
    
    @staticmethod
    def delete_directory(path: str, ignore_errors: bool = True) -> None:
        """
        Delete directory and its contents.
        
        Args:
            path: Directory path
            ignore_errors: Ignore errors during deletion
        """
        if Path(path).exists():
            shutil.rmtree(path, ignore_errors=ignore_errors)
    
    @staticmethod
    def copy_file(source: str, destination: str) -> None:
        """
        Copy file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
        """
        shutil.copy2(source, destination)
    
    @staticmethod
    def move_file(source: str, destination: str) -> None:
        """
        Move file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
        """
        shutil.move(source, destination)
    
    @staticmethod
    def delete_file(path: str) -> None:
        """
        Delete file.
        
        Args:
            path: File path
        """
        file_path = Path(path)
        if file_path.exists():
            file_path.unlink()
    
    @staticmethod
    def file_exists(path: str) -> bool:
        """
        Check if file exists.
        
        Args:
            path: File path
            
        Returns:
            True if file exists
        """
        return Path(path).is_file()
    
    @staticmethod
    def directory_exists(path: str) -> bool:
        """
        Check if directory exists.
        
        Args:
            path: Directory path
            
        Returns:
            True if directory exists
        """
        return Path(path).is_dir()
    
    @staticmethod
    def get_file_size(path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            path: File path
            
        Returns:
            File size in bytes
        """
        return Path(path).stat().st_size
    
    @staticmethod
    def list_files(
        directory: str,
        pattern: str = '*',
        recursive: bool = False
    ) -> List[str]:
        """
        List files in directory.
        
        Args:
            directory: Directory path
            pattern: File pattern (e.g., '*.txt')
            recursive: Search recursively
            
        Returns:
            List of file paths
        """
        path = Path(directory)
        
        if recursive:
            files = list(path.rglob(pattern))
        else:
            files = list(path.glob(pattern))
        
        return [str(f) for f in files if f.is_file()]
    
    @staticmethod
    def read_json(path: str) -> dict:
        """
        Read JSON file.
        
        Args:
            path: JSON file path
            
        Returns:
            Dictionary from JSON
        """
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def write_json(path: str, data: dict, indent: int = 2) -> None:
        """
        Write dictionary to JSON file.
        
        Args:
            path: JSON file path
            data: Dictionary to write
            indent: JSON indentation
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
    
    @staticmethod
    def get_absolute_path(path: str) -> str:
        """
        Get absolute path.
        
        Args:
            path: Relative or absolute path
            
        Returns:
            Absolute path
        """
        return str(Path(path).resolve())
    
    @staticmethod
    def get_file_extension(path: str) -> str:
        """
        Get file extension.
        
        Args:
            path: File path
            
        Returns:
            File extension (e.g., '.txt')
        """
        return Path(path).suffix
    
    @staticmethod
    def get_filename(path: str, with_extension: bool = True) -> str:
        """
        Get filename from path.
        
        Args:
            path: File path
            with_extension: Include file extension
            
        Returns:
            Filename
        """
        path_obj = Path(path)
        if with_extension:
            return path_obj.name
        return path_obj.stem