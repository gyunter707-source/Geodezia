#!/usr/bin/env python3
"""
Мастер экранов (wizard)
"""

import tkinter as tk
from tkinter import ttk
from screens.screen1_welcome import Screen1Welcome
from screens.screen2_format import Screen2Format
from screens.screen3_groups import Screen3Groups
from screens.screen4_layers import Screen4Layers
from screens.screen5_export import Screen5Export


class WizardApp:
    """Мастер экранов (wizard)."""
    
    SCREENS = {
        1: Screen1Welcome,
        2: Screen2Format,
        3: Screen3Groups,
        4: Screen4Layers,
        5: Screen5Export,
    }
    
    def __init__(self, root, state):
        self.root = root
        self.state = state
        self.current_screen = 1
        
        # Контейнер для экранов
        self.container = ttk.Frame(root)
        self.container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Кнопки навигации
        self.btn_frame = ttk.Frame(root)
        self.btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.btn_back = ttk.Button(
            self.btn_frame,
            text="Назад",
            command=self.go_back,
            state='disabled'
        )
        self.btn_back.pack(side='left')
        
        self.btn_next = ttk.Button(
            self.btn_frame,
            text="Далее",
            command=self.go_next,
            state='disabled'
        )
        self.btn_next.pack(side='right')
    
    def show_screen(self, screen_num):
        """Показывает указанный экран."""
        # Очищаем контейнер
        for widget in self.container.winfo_children():
            widget.destroy()
        
        self.current_screen = screen_num
        
        # Создаём экран
        screen_class = self.SCREENS[screen_num]
        screen = screen_class(self.container, self.state, self)
        screen.pack(fill='both', expand=True)
        
        # Обновляем кнопки
        self.update_nav_buttons()
    
    def go_next(self):
        """Переход к следующему экрану."""
        if self.current_screen < 5:
            self.show_screen(self.current_screen + 1)
    
    def go_back(self):
        """Переход к предыдущему экрану."""
        if self.current_screen > 1:
            self.show_screen(self.current_screen - 1)
    
    def update_nav_buttons(self):
        """Обновляет состояние кнопок навигации."""
        # Кнопка "Назад"
        self.btn_back['state'] = 'normal' if self.current_screen > 1 else 'disabled'
        
        # Кнопка "Далее"
        if self.current_screen == 5:
            self.btn_next['text'] = 'Сохранить DXF'
            self.btn_next['command'] = self.export_dxf
        else:
            self.btn_next['text'] = 'Далее'
            self.btn_next['command'] = self.go_next
        
        self.btn_next['state'] = self.state.get('can_go_next', 'disabled')
    
    def export_dxf(self):
        """Вызов экспорта DXF с последнего экрана."""
        # На экране 5 будет метод для экспорта
        screen_class = self.SCREENS[5]
        screen = self.container.winfo_children()[0]  # Получаем текущий экран
        if hasattr(screen, 'export_dxf'):
            screen.export_dxf()
    
    def set_can_go_next(self, can_go):
        """Устанавливает возможность перехода к следующему экрану."""
        self.state['can_go_next'] = 'normal' if can_go else 'disabled'
        self.update_nav_buttons()