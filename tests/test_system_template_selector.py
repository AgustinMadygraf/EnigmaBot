# tests/test_system_template_selector.py
import pytest
from utils.system_template_selector import SystemTemplateSelector

@pytest.fixture
def config():
    return {
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
def system_template_selector(config):
    return SystemTemplateSelector(config, input_func=lambda _: "1")

def test_seleccionar_system_template(system_template_selector):
    template = system_template_selector.seleccionar_system_template()
    assert "Responde siempre en español" in template
