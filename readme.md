# EnigmaBot

EnigmaBot es un asistente virtual diseñado para fortalecer la Gestión Obrera en Madygraf ex Donnelley, una fábrica recuperada por sus trabajadores en 2014. Este bot contribuye a mejorar el registro y control de la producción y distribución de bienes y servicios bajo gestión obrera.

## Características

- Asistente virtual en español.
- Registro y control de la producción y distribución.
- Selección dinámica de modelos según la capacidad de RAM.
- Plantillas de sistema personalizables.
- Historial de chat para mantener el contexto de la conversación.

## Estructura del Proyecto

```plaintext
EnigmaBot/
│
├── run.py
├── config/
│   ├── config.json
│   ├── logging.json
│   └── __init__.py
├── core/
│   ├── chatbot.py
│   ├── main.py
│   └── __init__.py
├── tests/
│   ├── test_chatbot.py
│   ├── test_integration.py
│   ├── test_model_selector.py
│   ├── test_ram_selector.py
│   ├── test_system_template_selector.py
│   └── __init__.py
├── utils/
│   ├── config_loader.py
│   ├── config_logger.py
│   ├── model_selector.py
│   ├── ram_selector.py
│   ├── system_template_selector.py
│   └── __init__.py
```

## Requisitos

- Python 3.8 o superior
- Paquetes listados en `requirements.txt`

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tu-AgustinMadygraf/enigmabot.git
    cd enigmabot
    ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

## Configuración

Edita el archivo `config/config.json` para personalizar las opciones de RAM y modelos disponibles, así como las plantillas del sistema.

## Uso

Para iniciar el bot, ejecuta:

```bash
python run.py
```

## Tests

Para ejecutar los tests, usa:

```bash
pytest
```

## Funcionalidades Clave

### Selección de RAM y Modelo

El bot permite seleccionar dinámicamente la capacidad de memoria RAM y el modelo de IA a utilizar. Esto se maneja a través de las clases `RamSelector` y `ModelSelector`.

### Plantillas del Sistema

El bot utiliza plantillas del sistema personalizables para definir su comportamiento. Estas plantillas se seleccionan al inicio de la sesión del bot.

### Historial del Chat

El historial del chat se mantiene para proporcionar contexto en las respuestas del bot. Esto se maneja dentro de la clase `ChatBot`.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue el flujo de trabajo estándar de GitHub para contribuir.

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu funcionalidad o corrección de bug (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios necesarios y confirma tus cambios (`git commit -m 'Añadir nueva funcionalidad'`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request en GitHub.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

