#EnigmaBot/tests/test_telegram_bot.py
import pytest
from core.telegram_bot import TelegramBot
from utils.config_loader import ConfigManager
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

@pytest.fixture
def config():
    config_manager = ConfigManager('config/config.json')
    return config_manager.config

def test_telegram_bot_start(config, monkeypatch):
    # Simular la entrada del usuario
    inputs = iter(["2", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    telegram_bot = TelegramBot(config, input_func=input)
    assert telegram_bot.token == os.getenv("TELEGRAM_TOKEN")
