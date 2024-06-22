# telegram_chatbot/run_bot.py
import sys
import os
os.system('cls' if os.name == 'nt' else 'clear')
import asyncio

# Asegúrate de que el directorio `src` esté en el `PYTHONPATH`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from core.main import main

if __name__ == '__main__':
    asyncio.run(main())
