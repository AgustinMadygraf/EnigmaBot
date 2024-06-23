# tests/test_model_selector.py
import pytest
from utils.model_selector import ModelSelector

@pytest.fixture
def config():
    return {
        "ram_options": {
            "1": "1 GB",
            "2": "4 GB",
            "3": "8 GB",
            "4": "16 GB"
        },
        "models_available": {
            "1 GB": ["all-MiniLM-L6-v2-f16.gguf"],
            "4 GB": ["replit-code-v1_5-3b-q4_0.gguf"],
            "8 GB": ["mistral-7b-openorca.Q4_0.gguf"],
            "16 GB": ["orca-2-13b.Q4_0.gguf"]
        }
    }

@pytest.fixture
def model_selector(config):
    return ModelSelector(config, "1 GB", input_func=lambda _: "1")

def test_seleccionar_modelo(model_selector):
    assert model_selector.seleccionar_modelo() == "all-MiniLM-L6-v2-f16.gguf"
