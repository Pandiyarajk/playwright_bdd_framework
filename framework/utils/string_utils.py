"""String utility functions."""

import re
import random
import string
from typing import List, Optional


class StringUtils:
    """String manipulation utilities."""
    
    @staticmethod
    def generate_random_string(
        length: int = 10,
        include_digits: bool = True,
        include_special: bool = False
    ) -> str:
        """
        Generate random string.
        
        Args:
            length: String length
            include_digits: Include digits
            include_special: Include special characters
            
        Returns:
            Random string
        """
        chars = string.ascii_letters
        
        if include_digits:
            chars += string.digits
        
        if include_special:
            chars += string.punctuation
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def generate_random_email(domain: str = 'example.com') -> str:
        """
        Generate random email address.
        
        Args:
            domain: Email domain
            
        Returns:
            Random email address
        """
        username = StringUtils.generate_random_string(10, include_special=False).lower()
        return f"{username}@{domain}"
    
    @staticmethod
    def remove_special_characters(
        text: str,
        keep_spaces: bool = True
    ) -> str:
        """
        Remove special characters from string.
        
        Args:
            text: Input string
            keep_spaces: Keep space characters
            
        Returns:
            Cleaned string
        """
        if keep_spaces:
            return re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return re.sub(r'[^a-zA-Z0-9]', '', text)
    
    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """
        Extract all numbers from string.
        
        Args:
            text: Input string
            
        Returns:
            List of numbers
        """
        numbers = re.findall(r'\d+', text)
        return [int(n) for n in numbers]
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Extract email addresses from string.
        
        Args:
            text: Input string
            
        Returns:
            List of email addresses
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def truncate(
        text: str,
        length: int,
        suffix: str = '...'
    ) -> str:
        """
        Truncate string to specified length.
        
        Args:
            text: Input string
            length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated string
        """
        if len(text) <= length:
            return text
        return text[:length - len(suffix)] + suffix
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in string.
        
        Args:
            text: Input string
            
        Returns:
            String with normalized whitespace
        """
        return ' '.join(text.split())
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """
        Convert string to snake_case.
        
        Args:
            text: Input string
            
        Returns:
            snake_case string
        """
        text = re.sub(r'[\s\-\.]+', '_', text)
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
        text = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', text)
        return text.lower()
    
    @staticmethod
    def to_camel_case(text: str) -> str:
        """
        Convert string to camelCase.
        
        Args:
            text: Input string
            
        Returns:
            camelCase string
        """
        components = text.split('_')
        return components[0].lower() + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def contains_ignore_case(text: str, substring: str) -> bool:
        """
        Case-insensitive substring check.
        
        Args:
            text: Text to search in
            substring: Substring to find
            
        Returns:
            True if substring found
        """
        return substring.lower() in text.lower()