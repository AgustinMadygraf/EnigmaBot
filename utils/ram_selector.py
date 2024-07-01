# utils/ram_selector.py
from tabulate import tabulate
from logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()
class RamSelector:
    def __init__(self, config, input_func=input):
        self.config = config
        self.input_func = input_func

    def seleccionar_memoria_ram(self):
        """
        Solicita al usuario seleccionar la capacidad de memoria RAM.
        """
        ram_options = self.config['ram_options']
        table_data = [[key, value] for key, value in ram_options.items()]
        table = tabulate(table_data, headers=["Opción", "Memoria RAM"], tablefmt="grid")
        print(table)

        opcion_ram = self.input_func("\nElige una opción: ")
        if opcion_ram == "":
            opcion_ram = "4"
        logger.info(f"Opción de RAM seleccionada: {opcion_ram}")
        return ram_options.get(opcion_ram, "2")
