#!/usr/bin/env python3
"""
Экран 2 - Настройка формата координат
"""

import tkinter as tk
from tkinter import ttk


class Screen2Format(ttk.Frame):
    """Экран 2: Настройка формата координат."""
    
    def __init__(self, parent, state, wizard):
        super().__init__(parent)
        self.state = state
        self.wizard = wizard
        
        # Значения по умолчанию
        self.x_value = tk.StringVar(value="")
        self.y_value = tk.StringVar(value="")
        self.z_value = tk.StringVar(value="")
        
        self.setup_ui()
        self.populate_data()
        self.auto_select_coords()  # Автоматически выбираем координаты
        self.check_selection()
    
    def setup_ui(self):
        """Настройка интерфейса экрана."""
        # Заголовок
        title_label = ttk.Label(
            self,
            text="Настройте формат координат",
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Рамка с искусственным примером
        example_frame = ttk.LabelFrame(self, text="Пример строки из файла", padding=15)
        example_frame.pack(fill='x', pady=(0, 20))
        
        # Искусственный пример
        example_text = "TOCHKA,  15.455,  31.455,  0.540"
        example_label = ttk.Label(
            example_frame,
            text=example_text,
            font=('Consolas', 11),
            foreground='#0066CC',
            background='#F0F0F0',
            padding=10
        )
        example_label.pack(fill='x')
        
        # Подсказка
        hint_label = ttk.Label(
            example_frame,
            text="Выберите числовые значения X, Y, Z из примера выше:",
            font=('Arial', 9),
            foreground='gray'
        )
        hint_label.pack(pady=(10, 0))
        
        # Рамка для выбора координат
        coords_frame = ttk.LabelFrame(self, text="Выбор координат", padding=15)
        coords_frame.pack(fill='x', pady=(0, 20))
        
        # Список значений будет заполнен в auto_select_coords()
        self.example_values = []
        
        # X
        x_frame = ttk.Frame(coords_frame)
        x_frame.pack(fill='x', pady=5)
        
        ttk.Label(x_frame, text="X =", font=('Arial', 10, 'bold'), width=8).pack(side='left')
        self.x_combo = ttk.Combobox(
            x_frame, 
            values=self.example_values, 
            textvariable=self.x_value,
            state='readonly',
            width=15
        )
        self.x_combo.pack(side='left', padx=(10, 0))
        self.x_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # Y
        y_frame = ttk.Frame(coords_frame)
        y_frame.pack(fill='x', pady=5)
        
        ttk.Label(y_frame, text="Y =", font=('Arial', 10, 'bold'), width=8).pack(side='left')
        self.y_combo = ttk.Combobox(
            y_frame, 
            values=self.example_values, 
            textvariable=self.y_value,
            state='readonly',
            width=15
        )
        self.y_combo.pack(side='left', padx=(10, 0))
        self.y_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # Z
        z_frame = ttk.Frame(coords_frame)
        z_frame.pack(fill='x', pady=5)
        
        ttk.Label(z_frame, text="Z =", font=('Arial', 10, 'bold'), width=8).pack(side='left')
        self.z_combo = ttk.Combobox(
            z_frame, 
            values=self.example_values, 
            textvariable=self.z_value,
            state='readonly',
            width=15
        )
        self.z_combo.pack(side='left', padx=(10, 0))
        self.z_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # Предупреждение о недопустимости одинаковых значений
        warning_label = ttk.Label(
            coords_frame,
            text="Внимание: координаты X, Y и Z не могут совпадать!",
            font=('Arial', 9),
            foreground='red'
        )
        warning_label.pack(pady=(15, 0))
        
        # Информация о том, что пример не влияет на данные
        info_label = ttk.Label(
            self,
            text="Примечание: пример служит только для визуального пояснения.\nРеальные данные берутся из вашего TXT файла (колонки 2, 3, 4).",
            font=('Arial', 8),
            foreground='gray',
            justify='center'
        )
        info_label.pack(pady=(20, 0))
    
    def populate_data(self):
        """Заполняет данные для анализа групп."""
        # DEBUG: выводим информацию о загруженных данных
        data = self.state.get('txt_data', [])
        print(f"DEBUG: populate_data() - loaded {len(data)} rows")
        if data:
            print(f"DEBUG: first row columns: {data[0]['columns']}")
    
    def auto_select_coords(self):
        """Автоматически выбирает координаты X, Y, Z из примера строки."""
        # Парсим числовые значения из примера строки
        example_text = "TOCHKA,  15.455,  31.455,  0.540"
        
        # Извлекаем числа из примера
        import re
        numbers = re.findall(r'-?\d+\.?\d*', example_text)
        
        print(f"DEBUG: Example text: '{example_text}'")
        print(f"DEBUG: Extracted numbers from example: {numbers}")
        
        if len(numbers) >= 3:
            # Используем первые 3 числа из примера
            example_values = numbers[:3]
            self.example_values = example_values
            
            # Обновляем combobox значения
            self.x_combo['values'] = example_values
            self.y_combo['values'] = example_values
            self.z_combo['values'] = example_values
            
            # Устанавливаем значения по умолчанию (разные)
            self.x_value.set(example_values[0])
            self.y_value.set(example_values[1])
            self.z_value.set(example_values[2])
            
            print(f"DEBUG: Auto-selected from example: X={example_values[0]}, Y={example_values[1]}, Z={example_values[2]}")
            
            # Проверяем выбор
            self.check_selection()
        else:
            print(f"DEBUG: Could not extract 3 numbers from example: {numbers}")
            # Фоллбек: пробуем загрузить из данных файла
            self._load_from_file_data()
    
    def _load_from_file_data(self):
        """Загружает координаты из данных файла (fallback)."""
        data = self.state.get('txt_data', [])
        if not data:
            print("DEBUG: No data available for fallback")
            return
        
        first_row = data[0].get('columns', [])
        if len(first_row) < 4:
            print(f"DEBUG: Not enough columns in first row: {first_row}")
            return
        
        # Находим 3 числовые колонки
        numeric_cols = []
        for i, val in enumerate(first_row[1:], 1):
            try:
                float(val)
                numeric_cols.append((i, val))
            except ValueError:
                pass
        
        if len(numeric_cols) >= 3:
            x_idx, x_val = numeric_cols[0][1]
            y_idx, y_val = numeric_cols[1][1]
            z_idx, z_val = numeric_cols[2][1]
            values = [v for _, v in numeric_cols[:10]]
        else:
            x_idx, y_idx, z_idx = 1, 2, 3
            x_val = first_row[x_idx] if len(first_row) > x_idx else ""
            y_val = first_row[y_idx] if len(first_row) > y_idx else ""
            z_val = first_row[z_idx] if len(first_row) > z_idx else ""
            values = [v for v in first_row[1:] if v][:10]
        
        self.example_values = values
        self.x_combo['values'] = values
        self.y_combo['values'] = values
        self.z_combo['values'] = values
        
        self.x_value.set(x_val)
        self.y_value.set(y_val)
        self.z_value.set(z_val)
        
        print(f"DEBUG: Fallback - loaded from file: X={x_val}, Y={y_val}, Z={z_val}")
        self.check_selection()
    
    def on_selection_change(self, event=None):
        """Обработка изменения выбора координат."""
        self.check_selection()
    
    def check_selection(self):
        """Проверяет правильность выбора координат."""
        x_val = self.x_value.get()
        y_val = self.y_value.get()
        z_val = self.z_value.get()
        
        print(f"DEBUG: check_selection() - X='{x_val}', Y='{y_val}', Z='{z_val}'")
        
        if x_val and y_val and z_val:
            # Проверяем, что все три значения разные
            values = [x_val, y_val, z_val]
            if len(set(values)) == 3:
                # Все значения выбраны и разные
                print("DEBUG: All values selected and different - proceeding")
                
                # Устанавливаем маппинг колонок (всегда: имя=0, X=1, Y=2, Z=3)
                self.state['column_mapping'] = {
                    'X': 1,  # Вторая колонка
                    'Y': 2,  # Третья колонка  
                    'Z': 3   # Четвёртая колонка
                }
                print(f"DEBUG: column_mapping set: {self.state['column_mapping']}")
                
                # Анализируем группы
                self.analyze_groups()
                
                # Разрешаем переход
                self.wizard.set_can_go_next(True)
                return
        
        # Если выбор некорректен
        print("DEBUG: Selection incomplete or invalid")
        self.wizard.set_can_go_next(False)
    
    def analyze_groups(self):
        """Анализирует группы точек на основе имени."""
        data = self.state.get('txt_data', [])
        column_mapping = self.state.get('column_mapping', {})
        
        print(f"DEBUG: analyze_groups() - data={len(data)}, mapping={column_mapping}")
        
        if not data or not column_mapping:
            print("DEBUG: No data or mapping - skipping groups analysis")
            return
        
        # Извлекаем группы из имен точек
        groups = {}
        
        for row in data:
            name = row['name']
            group = self.extract_group(name)
            print(f"DEBUG: Point '{name}' -> group '{group}'")
            
            # Пропускаем пустые и "UNKNOWN" группы
            if not group or group == "UNKNOWN":
                print(f"DEBUG: Skipping point '{name}' with group '{group}'")
                continue
            
            if group not in groups:
                groups[group] = {
                    'original': group,
                    'merged': group,  # По умолчанию итоговая группа = исходной
                    'points': []
                }
            groups[group]['points'].append(row)
        
        # Фильтруем: убираем "UNKNOWN" из groups_list
        groups_list = [
            g for g in list(groups.values())
            if g['original'] and g['original'] != "UNKNOWN"
        ]
        
        self.state['groups'] = groups_list
        
        print(f"DEBUG: Total unique groups found: {len(groups_list)}")
        print(f"DEBUG: groups = {groups_list}")
    
    def extract_group(self, name):
        """Извлекает буквенную часть из имени точки."""
        from utils.txt_parser import extract_group
        result = extract_group(name)
        # Возвращаем пустую строку если группа не найдена (НЕ "UNKNOWN")
        return result if result else ""