# tests/test_chatbot.py
import pytest
from core.chatbot import ChatBot

@pytest.fixture
def config():
    return {
        "model_path": "E:\\model_Explorer",
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

@pytest.fixture
def chatbot(config):
    return ChatBot(config, input_func=lambda _: "1")

def test_seleccionar_modelo(chatbot):
    chatbot.ram_seleccionada = "1 GB"
    assert chatbot.seleccionar_modelo() == "all-MiniLM-L6-v2-f16.gguf"

def test_seleccionar_system_template(chatbot):
    template = chatbot.seleccionar_system_template()
    assert "Responde siempre en español" in template
