# tests/test_app.py
import pytest
from src.app import main

@pytest.mark.asyncio
async def test_main(monkeypatch):
    class DummyConfigManager:
        def __init__(self, config_file):
            self.config = {
                "model_path": "E:\\Model _Explorer",
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
        def __init__(self, config, input_func=lambda _: "1"):
            self.config = config
            self.input_func = input_func
            self.ram_seleccionada = self.seleccionar_memoria_ram()
            self.modelo_seleccionado = self.seleccionar_modelo()
            self.model_path = config['model_path']
            self.model = None
            self.chat_histories = {}
            self.monitor_task = None
            self.system_template = self.seleccionar_system_template()

        def seleccionar_memoria_ram(self):
            return "1 GB"

        def seleccionar_modelo(self):
            return "all-MiniLM-L6-v2-f16.gguf"

        def seleccionar_system_template(self):
            return "### System:\nResponde siempre en español."

        async def iniciar_chat(self):
            pass

    monkeypatch.setattr('src.config_loader.ConfigManager', DummyConfigManager)
    monkeypatch.setattr('src.chatbot.ChatBot', DummyChatBot)

    await main(input_func=lambda _: "1")
