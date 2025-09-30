"""
Configuration Manager
Supports loading configuration from INI, JSON, and environment variables
"""

import os
import json
import configparser
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv


class ConfigManager:
    """Manages configuration from multiple sources (INI, JSON, environment)."""
    
    def __init__(self, config_file: Optional[str] = None, env: Optional[str] = None):
        """
        Initialize ConfigManager.
        
        Args:
            config_file: Path to configuration file (INI or JSON)
            env: Environment name (dev, test, staging, prod)
        """
        self.config_dir = Path(__file__).parent.parent.parent / "config"
        self.config_file = config_file
        self.env = env or os.getenv("ENV", "test")
        self.config_data: Dict[str, Any] = {}
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Load configurations
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from all available sources."""
        # 1. Load default INI config
        default_ini = self.config_dir / "config.ini"
        if default_ini.exists():
            self._load_ini(default_ini)
        
        # 2. Load environment-specific JSON config
        env_json = self.config_dir / f"{self.env}.json"
        if env_json.exists():
            self._load_json(env_json)
        
        # 3. Load custom config file if provided
        if self.config_file:
            config_path = Path(self.config_file)
            if config_path.exists():
                if config_path.suffix == ".ini":
                    self._load_ini(config_path)
                elif config_path.suffix == ".json":
                    self._load_json(config_path)
        
        # 4. Override with environment variables
        self._load_environment_variables()
    
    def _load_ini(self, file_path: Path) -> None:
        """Load configuration from INI file."""
        parser = configparser.ConfigParser()
        parser.read(file_path)
        
        for section in parser.sections():
            if section not in self.config_data:
                self.config_data[section] = {}
            
            for key, value in parser.items(section):
                # Handle environment variable substitution ${VAR_NAME}
                if value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    value = os.getenv(env_var, value)
                
                # Try to parse as JSON for complex types
                try:
                    value = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    pass
                
                self.config_data[section][key] = value
    
    def _load_json(self, file_path: Path) -> None:
        """Load configuration from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            
        # Merge JSON data into config_data
        for key, value in json_data.items():
            if isinstance(value, dict):
                if key not in self.config_data:
                    self.config_data[key] = {}
                self.config_data[key].update(value)
            else:
                self.config_data[key] = value
    
    def _load_environment_variables(self) -> None:
        """Load and override with environment variables."""
        # Common environment variable mappings
        env_mappings = {
            "BROWSER": ("framework", "browser"),
            "HEADLESS": ("framework", "headless"),
            "BASE_URL": ("framework", "base_url"),
            "TIMEOUT": ("framework", "timeout"),
            "JIRA_SERVER": ("jira", "server"),
            "JIRA_TOKEN": ("jira", "api_token"),
            "JIRA_EMAIL": ("jira", "email"),
            "ZEPHYR_TOKEN": ("zephyr", "api_token"),
            "DB_CONNECTION_STRING": ("database", "connection_string"),
            "SMTP_SERVER": ("email", "smtp_server"),
            "SMTP_PORT": ("email", "smtp_port"),
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                if section not in self.config_data:
                    self.config_data[section] = {}
                
                # Try to parse boolean and numeric values
                if value.lower() in ("true", "false"):
                    value = value.lower() == "true"
                elif value.isdigit():
                    value = int(value)
                
                self.config_data[section][key] = value
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        return self.config_data.get(section, {}).get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Configuration section name
            
        Returns:
            Dictionary of section configuration
        """
        return self.config_data.get(section, {})
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Configuration value
        """
        if section not in self.config_data:
            self.config_data[section] = {}
        self.config_data[section][key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration data.
        
        Returns:
            Complete configuration dictionary
        """
        return self.config_data
    
    def save_to_json(self, file_path: str) -> None:
        """
        Save current configuration to JSON file.
        
        Args:
            file_path: Path to save JSON file
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, indent=2)
    
    def __repr__(self) -> str:
        """String representation of ConfigManager."""
        return f"ConfigManager(env={self.env}, sections={list(self.config_data.keys())})"