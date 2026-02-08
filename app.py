#!/usr/bin/env python3
"""
Главное приложение Geodezia
"""

import tkinter as tk
from tkinter import ttk
from wizard import WizardApp


class GeodeziaApp:
    """Главное приложение Geodezia."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Geodezia - Конвертер тахеометрической съемки в DXF")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Установка иконки (если файл существует)
        try:
            self.root.iconbitmap('geodezia.ico')
        except tk.TclError:
            # Иконка не найдена или недоступна - продолжаем без неё
            pass
        
        # Стилизация
        style = ttk.Style()
        style.theme_use('clam')  # Используем тему clam для лучшего внешнего вида
        
        # Внутреннее состояние
        self.state = {
            'txt_file_path': None,
            'txt_data': [],
            'column_mapping': {},  # {'X': 0, 'Y': 1, 'Z': 2}
            'groups': [],          # [{'original': 'K', 'merged': 'K'}, ...]
            'layer_mapping': {},   # {'K': 'K', 'NIZR': 'NIZR_RIGEL'}
        }
        
        # Запускаем мастер
        self.wizard = WizardApp(self.root, self.state)
        self.wizard.show_screen(1)  # Первый экран
    
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = GeodeziaApp()
    app.run()