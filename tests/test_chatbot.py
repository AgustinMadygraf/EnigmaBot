#EnigmaBot/tests/test_chatbot.py
import pytest
from core.chatbot import ChatBot
from utils.database import connect_to_database

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

def test_save_message_to_db(chatbot):
    chatbot.save_message_to_db('Human', 'Hola, ¿cómo estás?')
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM chat_history WHERE session_id = %s", (chatbot.session_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    assert ('Human', 'Hola, ¿cómo estás?') in result

def test_seleccionar_memoria_ram(chatbot):
    assert chatbot.ram_seleccionada == "1 GB"
