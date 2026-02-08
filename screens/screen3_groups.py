#!/usr/bin/env python3
"""
Экран 3 - Анализ и объединение групп точек
"""

import tkinter as tk
from tkinter import ttk


class Screen3Groups(ttk.Frame):
    """Экран 3: Анализ и объединение групп точек."""

    def __init__(self, parent, state, wizard):
        super().__init__(parent)
        self.state = state
        self.wizard = wizard

        print("DEBUG: Screen3Groups.__init__ started")

        self.setup_ui()
        self.populate_groups_table()
        self.check_groups()

        print("DEBUG: Screen3Groups.__init__ completed")

    def setup_ui(self):
        """Настройка интерфейса экрана."""
        print("DEBUG: Screen3Groups.setup_ui() started")

        # Заголовок
        title_label = ttk.Label(
            self,
            text="Объедините группы точек",
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=(0, 10))

        # Инструкция
        instruction = ttk.Label(
            self,
            text="Для изменения итоговой группы выполните двойной щелчок по ячейке во втором столбце",
            font=('Arial', 10),
            foreground='#0066CC'
        )
        instruction.pack(pady=(0, 15))

        # Рамка с таблицей
        table_frame = ttk.LabelFrame(self, text="Группы точек", padding=10)
        table_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Настройка стиля Treeview
        style = ttk.Style()
        style.configure(
            'Groups.Treeview',
            rowheight=30,
            font=('Arial', 10),
            borderwidth=1,
            relief='solid'
        )
        style.configure(
            'Groups.Treeview.Heading',
            font=('Arial', 10, 'bold'),
            borderwidth=1,
            relief='solid'
        )
        style.theme_use('clam')

        # Создаем Treeview
        columns = ('original', 'merged')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=10,
            style='Groups.Treeview',
            selectmode='none'
        )

        # Настройка заголовков
        self.tree.heading('original', text='Исходная группа', anchor='center')
        self.tree.column('original', width=250, anchor='center', minwidth=150)

        self.tree.heading('merged', text='Итоговая группа', anchor='center')
        self.tree.column('merged', width=250, anchor='center', minwidth=150)

        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Упаковка - ВАЖНО: используем pack, а не grid
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Обработка двойного клика
        self.tree.bind('<Double-1>', self.on_double_click)

        # Примечание
        note_label = ttk.Label(
            self,
            text="Введите одинаковое имя в колонку 'Итоговая группа', чтобы объединить несколько групп в одну",
            font=('Arial', 9),
            foreground='gray',
            justify='center'
        )
        note_label.pack(pady=(5, 0))

        print("DEBUG: Screen3Groups.setup_ui() completed")

    def populate_groups_table(self):
        """Заполняет таблицу групп."""
        groups = self.state.get('groups', [])

        print(f"DEBUG: populate_groups_table() - {len(groups)} groups")

        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Если групп нет, показываем предупреждение
        if not groups:
            warning_label = ttk.Label(
                self,
                text="Группы не обнаружены. Проверьте формат файла или вернитесь назад.",
                font=('Arial', 11),
                foreground='red',
                justify='center'
            )
            warning_label.pack(fill='x', pady=20)
            print("DEBUG: No groups found - showed warning")
            return

        # Заполняем таблицу
        for group_info in groups:
            print(f"DEBUG: Adding group: {group_info}")
            self.tree.insert('', 'end', values=(
                group_info['original'],
                group_info['merged']
            ))

        print(f"DEBUG: Added {len(groups)} groups to table")

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
        groups = []
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, 'values')
            if values[0] != '-':
                groups.append({
                    'original': values[0],
                    'merged': values[1]
                })

        self.state['groups'] = groups
        print(f"DEBUG: Updated groups: {groups}")

    def check_groups(self, event=None):
        """Проверяет, есть ли группы, и обновляет возможность перехода."""
        groups = self.state.get('groups', [])
        has_groups = len(groups) > 0

        print(f"DEBUG: check_groups() - {len(groups)} groups, has_groups={has_groups}")

        if has_groups:
            layer_mapping = {}
            for group_info in groups:
                layer_mapping[group_info['original']] = group_info['merged']
            self.state['layer_mapping'] = layer_mapping
            print(f"DEBUG: Updated layer_mapping: {layer_mapping}")

        self.wizard.set_can_go_next(has_groups)
