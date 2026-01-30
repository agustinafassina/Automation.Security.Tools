"""
File utilities for reading and writing JSON and CSV files.
"""

import json
import csv
from pathlib import Path
from typing import Any, List, Dict
import logging

logger = logging.getLogger(__name__)


def read_json_file(file_path: str) -> Any:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise


def write_json_file(data: Any, file_path: str, indent: int = 4) -> None:
    """
    Write data to a JSON file.
    
    Args:
        data: Data to serialize to JSON
        file_path: Path where to write the file
        indent: JSON indentation level
        
    Raises:
        IOError: If file cannot be written
    """
    path = Path(file_path)
    
    try:
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        logger.info(f"JSON file written successfully: {file_path}")
    except Exception as e:
        logger.error(f"Error writing JSON file {file_path}: {e}")
        raise


def write_csv_file(data: List[Dict[str, Any]], file_path: str, fieldnames: List[str]) -> None:
    """
    Write data to a CSV file.
    
    Args:
        data: List of dictionaries to write
        file_path: Path where to write the file
        fieldnames: List of column names
        
    Raises:
        IOError: If file cannot be written
    """
    path = Path(file_path)
    
    try:
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in data:
                writer.writerow(row)
        logger.info(f"CSV file written successfully: {file_path}")
    except Exception as e:
        logger.error(f"Error writing CSV file {file_path}: {e}")
        raise

