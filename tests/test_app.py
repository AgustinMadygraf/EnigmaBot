# tests/test_app.py
import pytest
from src.app import main

@pytest.mark.asyncio
async def test_main(monkeypatch):
    class DummyConfigManager:
        def __init__(self, config_file):
            self.config = {
                "chat_history_path": "data/context_window_telegram.json"
            }
    
    class DummyChatBot:
        def __init__(self, config):
            pass

        async def iniciar_chat(self):
            pass

    monkeypatch.setattr('src.config_loader.ConfigManager', DummyConfigManager)
    monkeypatch.setattr('src.chatbot.ChatBot', DummyChatBot)

    await main()
