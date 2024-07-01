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

