#!/usr/bin/env python3
"""
Экран 4 - Названия DXF-слоёв
"""

import tkinter as tk
from tkinter import ttk


class Screen4Layers(ttk.Frame):
    """Экран 4: Названия DXF-слоёв."""

    def __init__(self, parent, state, wizard):
        super().__init__(parent)
        self.state = state
        self.wizard = wizard

        print("DEBUG: Screen4Layers.__init__ started")

        self.setup_ui()
        self.populate_layers_table()
        self.check_layers()

        print("DEBUG: Screen4Layers.__init__ completed")

    def setup_ui(self):
        """Настройка интерфейса экрана."""
        print("DEBUG: Screen4Layers.setup_ui() started")

        # Заголовок
        title_label = ttk.Label(
            self,
            text="Настройте имена DXF-слоёв",
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=(0, 10))

        # Инструкция
        instruction = ttk.Label(
            self,
            text="Для изменения имени слоя выполните двойной щелчок по ячейке во втором столбце",
            font=('Arial', 10),
            foreground='#0066CC'
        )
        instruction.pack(pady=(0, 15))

        # Рамка с таблицей
        table_frame = ttk.LabelFrame(self, text="Слои DXF", padding=10)
        table_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Настройка стиля
        style = ttk.Style()
        style.configure(
            'Layers.Treeview',
            rowheight=30,
            font=('Arial', 10),
            borderwidth=1,
            relief='solid'
        )
        style.configure(
            'Layers.Treeview.Heading',
            font=('Arial', 10, 'bold'),
            borderwidth=1,
            relief='solid'
        )
        style.theme_use('clam')

        # Создаем Treeview
        columns = ('group', 'layer')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=10,
            style='Layers.Treeview',
            selectmode='none'
        )

        # Настройка заголовков
        self.tree.heading('group', text='Итоговая группа', anchor='center')
        self.tree.column('group', width=250, anchor='center', minwidth=150)

        self.tree.heading('layer', text='Имя слоя DXF', anchor='center')
        self.tree.column('layer', width=250, anchor='center', minwidth=150)

        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Упаковка
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Обработка двойного клика
        self.tree.bind('<Double-1>', self.on_double_click)

        # Примечание
        note_label = ttk.Label(
            self,
            text="Введите понятные названия слоёв для удобства работы в AutoCAD",
            font=('Arial', 9),
            foreground='gray',
            justify='center'
        )
        note_label.pack(pady=(5, 0))

        print("DEBUG: Screen4Layers.setup_ui() completed")

    def populate_layers_table(self):
        """Заполняет таблицу слоёв."""
        groups = self.state.get('groups', [])

        print(f"DEBUG: populate_layers_table() - {len(groups)} groups")

        # Получаем уникальные итоговые группы
        unique_merged_groups = {}
        for group_info in groups:
            merged_name = group_info['merged']
            if merged_name not in unique_merged_groups:
                unique_merged_groups[merged_name] = group_info['original']

        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not unique_merged_groups:
            warning_label = ttk.Label(
                self,
                text="Нет групп для отображения. Вернитесь назад.",
                font=('Arial', 11),
                foreground='red',
                justify='center'
            )
            warning_label.pack(fill='x', pady=20)
            print("DEBUG: No layers found - showed warning")
            return

        # Заполняем таблицу
        for merged_name, original_name in unique_merged_groups.items():
            self.tree.insert('', 'end', values=(
                merged_name,  # Итоговая группа
                merged_name   # Имя слоя DXF (по умолчанию такое же)
            ))
            print(f"DEBUG: Added layer: {merged_name}")

    def on_double_click(self, event):
        """Обработка двойного клика для редактирования."""
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        selected_item = self.tree.focus()

        if not selected_item:
            return

        # Только вторая колонка редактируема
        if column == '#2':
            self.start_edit(selected_item, column)

    def start_edit(self, item, column):
        """Начинает редактирование ячейки."""
        bbox = self.tree.bbox(item, column)
        if not bbox:
            return

        x, y, width, height = bbox
        values = self.tree.item(item, 'values')

        entry = ttk.Entry(self.tree, font=('Arial', 10))
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, values[int(column[1]) - 1])
        entry.focus()

        def on_focus_out():
            self.finish_edit(item, column, entry)

        def on_enter_key(event):
            self.finish_edit(item, column, entry)

        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Return>", on_enter_key)
        entry.bind("<Escape>", lambda e: entry.destroy())

    def finish_edit(self, item, column, entry):
        """Завершает редактирование ячейки."""
        new_value = entry.get().strip()
        entry.destroy()

        if new_value:
            current_values = self.tree.item(item, 'values')
            new_values = list(current_values)
            new_values[int(column[1]) - 1] = new_value
            self.tree.item(item, values=new_values)

            self.update_state_from_table()

    def update_state_from_table(self):
        """Обновляет данные состояния из таблицы."""
        groups = self.state.get('groups', [])

        layer_mapping = {}
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            merged_group = values[0]
            layer_name = values[1]
            layer_mapping[merged_group] = layer_name

        updated_layer_mapping = {}
        for group_info in groups:
            original_group = group_info['original']
            merged_group = group_info['merged']
            layer_name = layer_mapping.get(merged_group, merged_group)
            updated_layer_mapping[original_group] = layer_name

        self.state['layer_mapping'] = updated_layer_mapping
        print(f"DEBUG: Updated layer_mapping: {updated_layer_mapping}")

    def check_layers(self, event=None):
        """Проверяет, есть ли слои, и обновляет возможность перехода."""
        layer_mapping = self.state.get('layer_mapping', {})
        has_layers = len(layer_mapping) > 0

        print(f"DEBUG: check_layers() - {len(layer_mapping)} layers, has_layers={has_layers}")

        self.wizard.set_can_go_next(has_layers)
