# utils/system_template_selector.py
from tabulate import tabulate

class SystemTemplateSelector:
    def __init__(self, config, input_func=input, logger=None):
        self.config = config
        self.input_func = input_func
        self.logger = logger

    def seleccionar_system_template(self):
        """
        Permite al usuario seleccionar un template de sistema para el chatbot.
        """
        system_templates = self.config['system_templates']
        table_data = [[idx + 1, template['mode']] for idx, template in enumerate(system_templates)]
        table = tabulate(table_data, headers=["#", "Modo"], tablefmt="grid")
        print(table)

        while True:
            try:
                seleccion_numero = self.input_func("\nSelecciona el número del template de sistema: ").strip()
                if seleccion_numero == "":
                    seleccion_numero = "1"
                seleccion_numero = int(seleccion_numero)
                if 1 <= seleccion_numero <= len(system_templates):
                    system_template = system_templates[seleccion_numero - 1]['template']
                    if self.logger:
                        self.logger.info(f"Template de sistema seleccionado: {system_templates[seleccion_numero - 1]['mode']}")
                    return system_template
                else:
                    print("Selección fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor ingresa un número.")
