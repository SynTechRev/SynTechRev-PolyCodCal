"""Tests for data loader functionality.

This module tests various data loading and processing operations.
"""

import json
from typing import Dict, List


class DataLoader:
    """Simple data loader for testing purposes."""

    def __init__(self, data_path: str):
        """Initialize the data loader.

        Args:
            data_path: Path to the data file
        """
        self.data_path = data_path
        self.data = []

    def load(self) -> List[Dict]:
        """Load data from file.

        Returns:
            List of data items
        """
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        return self.data

    def filter_by_key(self, key: str, value: str) -> List[Dict]:
        """Filter data by key-value pair.

        Args:
            key: Key to filter by
            value: Value to match

        Returns:
            Filtered list of items
        """
        return [item for item in self.data if item.get(key) == value]


def test_data_loader_initialization():
    """Test that DataLoader can be initialized with a path."""
    loader = DataLoader("/tmp/test.json")
    assert loader.data_path == "/tmp/test.json"
    assert loader.data == []


def test_data_loader_with_empty_file(tmp_path):
    """Test that DataLoader handles empty JSON files correctly."""
    test_file = tmp_path / "empty.json"
    test_file.write_text("[]")

    loader = DataLoader(str(test_file))
    data = loader.load()
    assert data == []


def test_data_loader_with_valid_data(tmp_path):
    """Test DataLoader with valid data."""
    test_file = tmp_path / "data.json"
    test_data = [
        {"id": 1, "name": "Alice", "status": "active"},
        {"id": 2, "name": "Bob", "status": "inactive"},
    ]
    test_file.write_text(json.dumps(test_data))

    loader = DataLoader(str(test_file))
    data = loader.load()
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"


def test_filter_by_key_returns_matching_items(tmp_path):
    """Test filter_by_key with matching items."""
    test_file = tmp_path / "data.json"
    test_data = [
        {"id": 1, "status": "active"},
        {"id": 2, "status": "inactive"},
        {"id": 3, "status": "active"},
    ]
    test_file.write_text(json.dumps(test_data))

    loader = DataLoader(str(test_file))
    loader.load()
    filtered = loader.filter_by_key("status", "active")

    assert len(filtered) == 2
    assert all(item["status"] == "active" for item in filtered)


def test_filter_by_key_with_no_matches(tmp_path):
    """Test filter_by_key when no items match the criteria."""
    test_file = tmp_path / "data.json"
    test_data = [
        {"id": 1, "status": "active"},
        {"id": 2, "status": "active"},
    ]
    test_file.write_text(json.dumps(test_data))

    loader = DataLoader(str(test_file))
    loader.load()
    filtered = loader.filter_by_key("status", "deleted")

    assert filtered == []


def test_filter_by_key_with_missing_key(tmp_path):
    """Test filter_by_key when items don't have the key."""
    test_file = tmp_path / "data.json"
    test_data = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "status": "active"},
    ]
    test_file.write_text(json.dumps(test_data))

    loader = DataLoader(str(test_file))
    loader.load()
    filtered = loader.filter_by_key("status", "active")

    assert len(filtered) == 1
    assert filtered[0]["id"] == 2
