import json

import pytest
from unittest.mock import mock_open, patch
from utils.services.config import ConfigManager

# Test data for various scenarios
test_data = [
    # ID: 1 - Happy path with valid data
    ("happy_path", {
        "AUTH": {"QB_USER": "user", "QB_PASSWD": "password"},
        "QB_URL": "http://localhost:8080",
        "QB_DEFAULT_SAVE_PATH": "/downloads"
    }, None),
    # ID: 2 - Edge case with minimal valid data
    ("minimal_valid", {
        "AUTH": {"QB_USER": "", "QB_PASSWD": ""},
        "QB_URL": "http://localhost:8080",
        "QB_DEFAULT_SAVE_PATH": "/downloads"
    }, None),
    # ID: 3 - Error case with missing AUTH key
    ("missing_auth", {
        "QB_URL": "http://localhost:8080",
        "QB_DEFAULT_SAVE_PATH": "/downloads"
    }, KeyError),
    # ID: 4 - Error case with missing QB_URL key
    ("missing_url", {
        "AUTH": {"QB_USER": "user", "QB_PASSWD": "password"},
        "QB_DEFAULT_SAVE_PATH": "/downloads"
    }, KeyError),
    # ID: 5 - Error case with missing QB_DEFAULT_SAVE_PATH key
    ("missing_save_path", {
        "AUTH": {"QB_USER": "user", "QB_PASSWD": "password"},
        "QB_URL": "http://localhost:8080"
    }, KeyError)
]


@pytest.mark.parametrize("test_id, config_data, expected_exception", test_data, ids=[td[0] for td in test_data])
def test_config_manager(test_id, config_data, expected_exception):
    # Arrange
    m = mock_open(read_data=json.dumps(config_data))
    with patch("builtins.open", m):
        if expected_exception:
            # Act & Assert
            with pytest.raises(expected_exception):
                ConfigManager()
        else:
            # Act
            config_manager = ConfigManager()

            # Assert
            assert config_manager.QBITTORRENT_AUTH == (config_data["AUTH"]["QB_USER"], config_data["AUTH"]["QB_PASSWD"])
            assert config_manager.QBITTORRENT_URL == config_data["QB_URL"]
            assert config_manager.QB_DEFAULT_SAVE_PATH == config_data["QB_DEFAULT_SAVE_PATH"]
