# tests/test_integration.py
import pytest
from src.config_loader import ConfigManager
from src.chatbot import ChatBot

@pytest.fixture
def config_manager():
    return ConfigManager('config.json')

@pytest.fixture
def chatbot(config_manager):
    return ChatBot(config_manager.config)

@pytest.mark.asyncio
async def test_iniciar_chat(chatbot, monkeypatch):
    async def mock_ciclo_principal_chat(chat_id):
        pass

    monkeypatch.setattr(chatbot, 'ciclo_principal_chat', mock_ciclo_principal_chat)
    await chatbot.iniciar_chat()
