#!/usr/bin/env python3
"""
Тестовый запуск приложения
"""

import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import GeodeziaApp
    print("Запуск Geodezia приложения...")
    app = GeodeziaApp()
    app.run()
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что все зависимости установлены: pip install -r requirements.txt")
except Exception as e:
    print(f"Ошибка запуска: {e}")