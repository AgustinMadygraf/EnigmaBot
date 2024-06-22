# tests/test_app.py
import pytest
from src.app import main

@pytest.mark.asyncio
async def test_main(monkeypatch):
    class DummyConfigManager:
        def __init__(self, config_file):
            self.config = {
                "chat_history_path": "data/context_window_telegram.json",
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
                },
                "system_templates": [
                    {
                        "mode": "ingeniero virtual",
                        "template": "### System:\nResponde siempre en español."
                    },
                    {
                        "mode": "genérico",
                        "template": "### System:\nResponde siempre en español."
                    }
                ]
            }

    class DummyChatBot:
        def __init__(self, config, input_func):
            pass

        async def iniciar_chat(self):
            pass

    async def dummy_main(input_func):
        config_manager = DummyConfigManager("config.json")
        config = config_manager.config
        chatbot = DummyChatBot(config, input_func=input_func)
        await chatbot.iniciar_chat()

    monkeypatch.setattr('src.config_loader.ConfigManager', DummyConfigManager)
    monkeypatch.setattr('src.chatbot.ChatBot', DummyChatBot)

    await dummy_main(input_func=lambda _: "1")

