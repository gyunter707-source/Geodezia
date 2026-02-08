#!/usr/bin/env python3
"""
Экран 1 - Загрузка TXT файла
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


class Screen1Welcome(ttk.Frame):
    """Экран 1: Загрузка TXT файла тахеометрической съемки."""
    
    def __init__(self, parent, state, wizard):
        super().__init__(parent)
        self.state = state
        self.wizard = wizard
        
        self.setup_ui()
        self.check_file_loaded()
    
    def setup_ui(self):
        """Настройка интерфейса экрана."""
        # Заголовок
        title_label = ttk.Label(
            self,
            text="Загрузите TXT-файл тахеометрической съемки",
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Кнопка выбора файла
        self.select_btn = ttk.Button(
            self,
            text="Выбрать TXT файл",
            command=self.select_file
        )
        self.select_btn.pack(pady=10)
        
        # Статус загрузки
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(pady=20, fill='x')
        
        self.status_icon = ttk.Label(self.status_frame, text="❌", font=('Arial', 16))
        self.status_icon.pack(side='left', padx=(0, 10))
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="TXT файл не загружен",
            font=('Arial', 10)
        )
        self.status_label.pack(side='left')
    
    def select_file(self):
        """Выбор TXT файла."""
        file_path = filedialog.askopenfilename(
            title="Выберите TXT файл тахеометрической съемки",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            if not self.validate_txt_file(file_path):
                messagebox.showerror(
                    "Ошибка",
                    "Выбранный файл не является корректным TXT файлом тахеометрической съемки.\n"
                    "Файл должен содержать строки в формате: ИМЯ_ТОЧКИ,X,Y,Z,"
                )
                return
            
            # Сохраняем путь и данные файла
            self.state['txt_file_path'] = file_path
            self.state['txt_data'] = self.load_txt_data(file_path)
            
            # Обновляем статус
            self.update_status(True, file_path)
            
            # Проверяем возможность перехода к следующему экрану
            self.check_file_loaded()
    
    def validate_txt_file(self, file_path):
        """Проверяет, является ли файл корректным TXT файлом."""
        try:
            # Проверяем расширение
            if not file_path.lower().endswith('.txt'):
                return False
            
            # Используем валидатор из модуля txt_parser
            from utils.txt_parser import validate_txt_content
            return validate_txt_content(file_path)
                
        except Exception:
            return False
    
    def load_txt_data(self, file_path):
        """Загружает данные из TXT файла."""
        try:
            from utils.txt_parser import parse_txt
            return parse_txt(file_path)
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            return []
    
    def update_status(self, loaded, file_path=""):
        """Обновляет статус загрузки."""
        if loaded:
            filename = os.path.basename(file_path)
            self.status_icon.config(text="✅")
            self.status_label.config(
                text=f"TXT файл загружен: {filename}",
                foreground='green'
            )
        else:
            self.status_icon.config(text="❌")
            self.status_label.config(
                text="TXT файл не загружен",
                foreground='black'
            )
    
    def check_file_loaded(self):
        """Проверяет, загружен ли файл, и обновляет возможность перехода."""
        file_loaded = bool(self.state.get('txt_file_path'))
        self.wizard.set_can_go_next(file_loaded)