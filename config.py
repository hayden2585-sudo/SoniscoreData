#!/usr/bin/env python3
"""
SoniscoreData - Configuration module.
Defines default settings and constants.
"""

import os
from pathlib import Path
from typing import Dict, Any


# Default configuration
DEFAULT_CONFIG = {
    'data': {
        'input_dir': './data',
        'output_dir': './output',
        'default_format': 'csv',
        'max_file_size_mb': 100
    },
    'processing': {
        'normalize_method': 'minmax',
        'missing_value_strategy': 'median',
        'outlier_threshold': 3.0
    },
    'scoring': {
        'default_weight': 1.0,
        'score_precision': 4
    },
    'visualization': {
        'dpi': 150,
        'format': 'png',
        'style': 'seaborn-v0_8-whitegrid'
    },
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
}


def get_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from file or return defaults.
    
    Args:
        config_path: Path to configuration file (YAML/JSON)
    
    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_path and os.path.exists(config_path):
        try:
            import yaml
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f)
            config.update(file_config)
        except ImportError:
            # Try JSON
            try:
                import json
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                config.update(file_config)
            except ImportError:
                print("Warning: Could not load config file. Using defaults.")
        except Exception as e:
            print(f"Warning: Error loading config: {e}. Using defaults.")
    
    return config


def get_data_dirs(config: Dict[str, Any] = None) -> Dict[str, Path]:
    """
    Get data directories from config.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Dictionary with input and output paths
    """
    if config is None:
        config = get_config()
    
    data_dir = Path(config['data']['input_dir'])
    output_dir = Path(config['data']['output_dir'])
    
    # Create directories if they don't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return {
        'input': data_dir,
        'output': output_dir
    }


if __name__ == '__main__':
    config = get_config()
    print("SoniscoreData configuration module loaded successfully")
    print(f"Default config: {config}")