#!/usr/bin/env python3
"""
Storage Module - Handles JSON file operations for data persistence.

This module provides functions for loading and saving data to a JSON file,
ensuring data integrity and proper file handling.

Author: [Your Name]
Version: 1.0.0
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

# Default data file path
DATA_FILE = "data.json"

# Default data structure
DEFAULT_DATA = {
    "total_income": 0.0,
    "total_expense": 0.0,
    "balance": 0.0,
    "transactions": [],
    "created_at": "",
    "last_updated": ""
}


def get_data_file_path() -> str:
    """
    Get the absolute path to the data file.
    
    Returns:
        str: Absolute path to the data.json file.
    
    Example:
        >>> path = get_data_file_path()
        >>> print(path)
        '/path/to/smart-expense-tracker/data.json'
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, DATA_FILE)


def initialize_data_file() -> bool:
    """
    Initialize the data file if it doesn't exist.
    
    Creates a new data.json file with default structure if one
    doesn't already exist.
    
    Returns:
        bool: True if file was created or already exists, False on error.
    
    Example:
        >>> success = initialize_data_file()
        >>> print(success)
        True
    """
    file_path = get_data_file_path()
    
    if os.path.exists(file_path):
        # Validate existing file
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Check if it has required keys
                if all(key in data for key in DEFAULT_DATA.keys()):
                    return True
        except (json.JSONDecodeError, IOError):
            pass
    
    # Create new file with default data
    try:
        default_data = DEFAULT_DATA.copy()
        default_data["created_at"] = datetime.now().isoformat()
        default_data["last_updated"] = datetime.now().isoformat()
        
        with open(file_path, 'w') as f:
            json.dump(default_data, f, indent=4)
        
        return True
    except IOError as e:
        print(f"Error creating data file: {e}")
        return False


def load_data() -> Dict[str, Any]:
    """
    Load data from the JSON file.
    
    Returns:
        Dict[str, Any]: Dictionary containing all stored data.
                       Returns default data structure if file doesn't exist
                       or is corrupted.
    
    Example:
        >>> data = load_data()
        >>> print(data["balance"])
        1500.00
    """
    file_path = get_data_file_path()
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Ensure all required keys exist
                for key, default_value in DEFAULT_DATA.items():
                    if key not in data:
                        data[key] = default_value
                
                return data
    except json.JSONDecodeError as e:
        print(f"Warning: Data file is corrupted. Creating backup and starting fresh.")
        # Create backup of corrupted file
        if os.path.exists(file_path):
            backup_path = file_path + ".backup"
            os.rename(file_path, backup_path)
    except IOError as e:
        print(f"Warning: Could not read data file: {e}")
    
    # Return default data if file doesn't exist or is corrupted
    return DEFAULT_DATA.copy()


def save_data(data: Dict[str, Any]) -> bool:
    """
    Save data to the JSON file.
    
    Args:
        data: Dictionary containing all data to save.
    
    Returns:
        bool: True if save was successful, False otherwise.
    
    Example:
        >>> data = load_data()
        >>> data["balance"] = 2000.00
        >>> success = save_data(data)
        >>> print(success)
        True
    """
    file_path = get_data_file_path()
    temp_path = None
    
    try:
        # Update last_updated timestamp
        data["last_updated"] = datetime.now().isoformat()
        
        # Write to a temporary file first (atomic write)
        temp_path = file_path + ".tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Replace original file with temporary file
        os.replace(temp_path, file_path)
        
        return True
    except IOError as e:
        print(f"Error saving data: {e}")
        # Clean up temporary file if it exists and was created
        if temp_path is not None and os.path.exists(temp_path):
            os.remove(temp_path)
        return False


def backup_data(backup_filename: Optional[str] = None) -> bool:
    """
    Create a backup of the current data file.
    
    Args:
        backup_filename: Optional custom filename for the backup.
                        If not provided, uses timestamp-based name.
    
    Returns:
        bool: True if backup was successful, False otherwise.
    
    Example:
        >>> success = backup_data()
        >>> print(success)
        True
    """
    file_path = get_data_file_path()
    
    if not os.path.exists(file_path):
        print("No data file to backup.")
        return False
    
    if backup_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"data_backup_{timestamp}.json"
    
    backup_path = os.path.join(os.path.dirname(file_path), backup_filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        return True
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error creating backup: {e}")
        return False


def clear_all_data() -> bool:
    """
    Clear all data and reset to default state.
    
    Warning: This action is irreversible!
    
    Returns:
        bool: True if data was cleared successfully, False otherwise.
    
    Example:
        >>> success = clear_all_data()
        >>> print(success)
        True
    """
    try:
        default_data = DEFAULT_DATA.copy()
        default_data["created_at"] = datetime.now().isoformat()
        default_data["last_updated"] = datetime.now().isoformat()
        
        return save_data(default_data)
    except Exception as e:
        print(f"Error clearing data: {e}")
        return False


def get_data_statistics() -> Dict[str, Any]:
    """
    Get statistics about the stored data.
    
    Returns:
        Dict[str, Any]: Dictionary containing data statistics.
    
    Example:
        >>> stats = get_data_statistics()
        >>> print(stats["total_transactions"])
        50
    """
    data = load_data()
    
    transactions = data.get("transactions", [])
    
    income_count = len([t for t in transactions if t.get("type") == "income"])
    expense_count = len([t for t in transactions if t.get("type") == "expense"])
    
    return {
        "total_transactions": len(transactions),
        "income_transactions": income_count,
        "expense_transactions": expense_count,
        "total_income": data.get("total_income", 0.0),
        "total_expense": data.get("total_expense", 0.0),
        "balance": data.get("balance", 0.0),
        "created_at": data.get("created_at", "Unknown"),
        "last_updated": data.get("last_updated", "Unknown")
    }