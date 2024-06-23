# tests/test_ram_selector.py
import pytest
from utils.ram_selector import RamSelector

@pytest.fixture
def config():
    return {
        "ram_options": {
            "1": "1 GB",
            "2": "4 GB",
            "3": "8 GB",
            "4": "16 GB"
        }
    }

@pytest.fixture
def ram_selector(config):
    return RamSelector(config, input_func=lambda _: "1")

def test_seleccionar_memoria_ram(ram_selector):
    assert ram_selector.seleccionar_memoria_ram() == "1 GB"
