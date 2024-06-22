# tests/test_chatbot.py
import pytest
from src.chatbot import ChatBot

@pytest.fixture
def config():
    return {
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

@pytest.fixture
def chatbot(config):
    return ChatBot(config)

def test_seleccionar_memoria_ram(chatbot, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2")
    assert chatbot.seleccionar_memoria_ram() == "4 GB"

def test_seleccionar_modelo(chatbot, monkeypatch):
    chatbot.ram_seleccionada = "4 GB"
    monkeypatch.setattr('builtins.input', lambda _: "1")
    assert chatbot.seleccionar_modelo() == "replit-code-v1_5-3b-q4_0.gguf"

def test_seleccionar_system_template(chatbot, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    template = chatbot.seleccionar_system_template()
    assert "Responde siempre en español" in template
