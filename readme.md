# MadyBot

## Descripción
MadyBot es un proyecto cuyo objetivo es experimentar con la interacción a través de Telegram con un ChatBot conversacional basado en modelos de lenguaje grande (LLM) y entrenarlo para mejorar su desempeño. Este proyecto está desarrollado en Python.

## Estructura de Carpetas y Archivos

```plaintext
MadyBot/
    readme.md
    run.py
    config/
        config.json
        __init__.py
        data/
            training_data.json
    core/
        chatbot.py
        main.py
        telegram_bot.py
        telegram_command_handler.py
        telegram_message_handler.py
        __init__.py
    logs/
        config_logger.py
        logging.json
    tests/
        test_chatbot.py
        test_config_loader.py
        test_integration.py
        test_model_selector.py
        test_ram_selector.py
        test_system_template_selector.py
        test_telegram_bot.py
        __init__.py
    utils/
        config_loader.py
        database.py
        model_selector.py
        ram_selector.py
        system_template_selector.py
        __init__.py
```

## Instalación
1. Clona el repositorio:
    ```bash
    git clone https://github.com/AgustinMadygraf/MadyBot.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd MadyBot
    ```
3. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración
Asegúrate de configurar las variables necesarias en `config/config.json` y en el archivo `.env` (si lo utilizas) para que el bot pueda funcionar correctamente.

## Uso
Para iniciar el bot:
```bash
python run.py
```

## Estructura del Código
- **run.py**: Archivo principal para ejecutar el bot.
- **config/**: Contiene archivos de configuración.
- **core/**: Componentes principales del bot como la lógica del chatbot y la integración con Telegram.
- **docs/**: Documentación adicional del proyecto.
- **logs/**: Configuraciones y archivos de registro.
- **tests/**: Pruebas unitarias para asegurar la calidad del código.
- **utils/**: Utilidades y funciones auxiliares utilizadas por el bot.

## Contribuir
Si deseas contribuir a este proyecto, por favor sigue estos pasos:
1. Haz un fork del proyecto.
2. Crea una rama nueva (`git checkout -b feature-nueva`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva característica'`).
4. Sube tu rama (`git push origin feature-nueva`).
5. Crea un nuevo Pull Request.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.