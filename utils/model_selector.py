# utils/model_selector.py
from tabulate import tabulate

class ModelSelector:
    def __init__(self, config, ram_seleccionada, input_func=input, logger=None):
        self.config = config
        self.ram_seleccionada = ram_seleccionada
        self.input_func = input_func
        self.logger = logger

    def seleccionar_modelo(self):
        """
        Permite al usuario seleccionar un modelo de IA basado en la capacidad de RAM seleccionada.
        """
        modelos_a_mostrar = self.obtener_modelos_disponibles()
        self.mostrar_opciones_modelo(modelos_a_mostrar)
        return self.obtener_seleccion_modelo(modelos_a_mostrar)

    def obtener_modelos_disponibles(self):
        """
        Obtiene la lista de modelos disponibles según la RAM seleccionada.
        """
        return self.config['models_available'].get(self.ram_seleccionada, [])

    def mostrar_opciones_modelo(self, modelos):
        """
        Muestra los modelos de IA disponibles al usuario.
        """
        if modelos:
            if self.logger:
                self.logger.info("Modelos disponibles:")
            table_data = [[idx + 1, modelo] for idx, modelo in enumerate(modelos)]
            table = tabulate(table_data, headers=["#", "Modelo"], tablefmt="grid")
            print(table)

    def obtener_seleccion_modelo(self, modelos):
        """
        Obtiene la selección del usuario de entre los modelos disponibles.
        """
        while True:
            try:
                seleccion_numero = self.input_func("\nSelecciona el número del modelo: ").strip()
                if seleccion_numero == "":
                    seleccion_numero = "2"
                seleccion_numero = int(seleccion_numero)
                if 1 <= seleccion_numero <= len(modelos):
                    modelo_seleccionado = modelos[seleccion_numero - 1]
                    if self.logger:
                        self.logger.info(f"Modelo seleccionado: {modelo_seleccionado}")
                    return modelo_seleccionado
                else:
                    print("Selección fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor ingresa un número.")
