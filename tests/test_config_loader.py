import pytest
from utils.config_loader import ConfigManager
from unittest.mock import patch, mock_open
import json

# Test para la carga correcta de la configuración
def test_carga_correcta():
    # Simulación de datos de configuración válidos
    data = {
        "model_path": "path/to/model",
        "chat_history_path": "path/to/history.json"
    }
    with patch('builtins.open', mock_open(read_data=json.dumps(data))):
        config_manager = ConfigManager("fake_path")
        assert config_manager.config == data, "La configuración debe coincidir con los datos simulados"

# Test para archivo de configuración no encontrado
def test_archivo_no_encontrado():
    with pytest.raises(SystemExit) as e:
        with patch('builtins.open', side_effect=FileNotFoundError()):
            ConfigManager("fake_path")
    assert str(e.value) == "Error: Archivo de configuración no encontrado."

# Test para contenido corrupto en archivo de configuración
def test_contenido_corrupto():
    with pytest.raises(SystemExit) as e:
        with patch('builtins.open', mock_open(read_data="no json")):
            ConfigManager("fake_path")
    assert "Error: Formato de archivo de configuración inválido." in str(e.value)

# Test para verificación de permisos de archivo
def test_permiso_denegado():
    with pytest.raises(SystemExit) as e:
        with patch('builtins.open', side_effect=PermissionError()):
            ConfigManager("fake_path")
    assert str(e.value) == "Error: Permiso denegado."
