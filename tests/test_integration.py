# tests/test_integration.py
import pytest
import asyncio
from core.chatbot import ChatBot
from utils.config_loader import ConfigManager

@pytest.fixture
def config():
    config_manager = ConfigManager('config/config.json')
    return config_manager.config

@pytest.fixture
def chatbot(config):
    return ChatBot(config, input_func=lambda _: "1")

@pytest.mark.asyncio
async def test_iniciar_chat_consola(chatbot, monkeypatch):
    async def mock_ciclo_principal_chat(chat_id):
        pass  # Simular la ejecución del ciclo de chat sin necesidad de interacción real

    monkeypatch.setattr(chatbot, 'ciclo_principal_chat', mock_ciclo_principal_chat)
    await chatbot.iniciar_chat_consola()
