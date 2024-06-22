# tests/test_config_loader.py
import pytest
import json
import io
from src.config_loader import ConfigManager

def test_cargar_configuracion_correcta(monkeypatch):
    dummy_config = {
        "model_path": "E:\\Model _Explorer",
        "chat_history_path": "data/context_window_telegram.json",
        "ram_options": {
            "1": "1 GB",
            "2": "4 GB",
            "3": "8 GB",
            "4": "16 GB"
        }
    }

    def mock_open(*args, **kwargs):
        if args[0] == 'config.json':
            return io.StringIO(json.dumps(dummy_config))
        return open(*args, **kwargs)

    monkeypatch.setattr('builtins.open', mock_open)

    config_manager = ConfigManager('config.json')
    assert config_manager.config == dummy_config

def test_archivo_no_encontrado(monkeypatch):
    def mock_open(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr('builtins.open', mock_open)

    with pytest.raises(SystemExit):
        ConfigManager('config.json')

def test_json_decode_error(monkeypatch):
    def mock_open(*args, **kwargs):
        return io.StringIO("invalid json")

    monkeypatch.setattr('builtins.open', mock_open)

    with pytest.raises(SystemExit):
        ConfigManager('config.json')

def test_permission_error(monkeypatch):
    def mock_open(*args, **kwargs):
        raise PermissionError

    monkeypatch.setattr('builtins.open', mock_open)

    with pytest.raises(SystemExit):
        ConfigManager('config.json')
