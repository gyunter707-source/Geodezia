#!/usr/bin/env python3
"""
Экран 5 - Экспорт DXF
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


class Screen5Export(ttk.Frame):
    """Экран 5: Экспорт DXF."""
    
    def __init__(self, parent, state, wizard):
        super().__init__(parent)
        self.state = state
        self.wizard = wizard
        
        self.setup_ui()
        self.check_export_ready()
    
    def setup_ui(self):
        """Настройка интерфейса экрана."""
        # Заголовок
        title_label = ttk.Label(
            self,
            text="Экспорт в DXF файл",
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Информация о данных
        info_frame = ttk.LabelFrame(self, text="Информация о данных", padding=10)
        info_frame.pack(fill='x', pady=(0, 20))
        
        # Подсчет точек и слоев
        total_points = len(self.state.get('txt_data', []))
        total_groups = len(set(g['merged'] for g in self.state.get('groups', [])))
        total_layers = len(set(self.state.get('layer_mapping', {}).values()))
        
        ttk.Label(info_frame, text=f"Всего точек: {total_points}", font=('Arial', 10)).pack(anchor='w')
        ttk.Label(info_frame, text=f"Всего групп: {total_groups}", font=('Arial', 10)).pack(anchor='w')
        ttk.Label(info_frame, text=f"Всего слоёв: {total_layers}", font=('Arial', 10)).pack(anchor='w')
        
        # Кнопка сохранения
        self.export_btn = ttk.Button(
            self,
            text="Сохранить DXF файл",
            command=self.export_dxf,
            state='disabled'
        )
        self.export_btn.pack(pady=10)
        
        # Статус
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(pady=20, fill='x')
        
        self.status_icon = ttk.Label(self.status_frame, text="", font=('Arial', 16))
        self.status_icon.pack(side='left', padx=(0, 10))
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Готов к экспорту",
            font=('Arial', 10)
        )
        self.status_label.pack(side='left')
    
    def check_export_ready(self):
        """Проверяет, готовы ли данные к экспорту."""
        txt_data = self.state.get('txt_data', [])
        column_mapping = self.state.get('column_mapping', {})
        layer_mapping = self.state.get('layer_mapping', {})
        
        ready = len(txt_data) > 0 and len(column_mapping) == 3 and len(layer_mapping) > 0
        
        if ready:
            self.export_btn['state'] = 'normal'
            self.wizard.set_can_go_next(True)
        else:
            self.export_btn['state'] = 'disabled'
            self.wizard.set_can_go_next(False)
    
    def export_dxf(self):
        """Экспорт данных в DXF файл."""
        # Диалог выбора файла
        file_path = filedialog.asksaveasfilename(
            title="Сохранить DXF файл",
            defaultextension=".dxf",
            filetypes=[("DXF files", "*.dxf"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Проверяем, что все необходимые данные есть
            if not self.state.get('txt_data'):
                messagebox.showerror("Ошибка", "Нет данных для экспорта. Загрузите TXT файл.")
                return
            
            if not self.state.get('column_mapping'):
                messagebox.showerror("Ошибка", "Не настроены координаты. Перейдите к предыдущим шагам.")
                return
            
            if not self.state.get('layer_mapping'):
                messagebox.showerror("Ошибка", "Не настроены слои. Перейдите к предыдущим шагам.")
                return
            
            # Показываем процесс экспорта
            self.update_status("", "Выполняется экспорт...")
            self.export_btn.config(state='disabled')
            self.update()
            
            # Импортируем модуль экспорта
            try:
                from utils.dxf_exporter import create_dxf
            except ImportError as e:
                raise ImportError(f"Модуль ezdxf не установлен: {e}")
            
            # Выполняем экспорт
            print(f"DEBUG: Exporting with column_mapping={self.state['column_mapping']}")
            print(f"DEBUG: Exporting with layer_mapping={self.state['layer_mapping']}")
            print(f"DEBUG: Exporting {len(self.state['txt_data'])} points")
            
            success = create_dxf(
                output_path=file_path,
                points_data=self.state['txt_data'],
                column_mapping=self.state['column_mapping'],
                layer_mapping=self.state['layer_mapping'],
                point_type='CIRCLE'
            )
            
            if success:
                self.update_status("✅", f"DXF успешно создан: {os.path.basename(file_path)}")
                messagebox.showinfo("Успех", f"DXF файл успешно создан:\n{file_path}")
            else:
                self.update_status("❌", "Ошибка при создании DXF файла")
                messagebox.showerror("Ошибка", "Не удалось создать DXF файл. Проверьте данные.")
                
        except ImportError as e:
            error_msg = f"Ошибка импорта: {str(e)}\n\nДля установки зависимостей выполните:\npip install -r requirements.txt"
            print(f"DEBUG: {error_msg}")
            self.update_status("❌", "Отсутствует ezdxf")
            messagebox.showerror("Ошибка импорта", error_msg)
        except Exception as e:
            error_msg = f"Ошибка при экспорте: {type(e).__name__}: {str(e)}"
            print(f"DEBUG: {error_msg}")
            import traceback
            traceback.print_exc()
            self.update_status("❌", f"Ошибка: {type(e).__name__}")
            messagebox.showerror("Ошибка", error_msg)
        finally:
            self.export_btn.config(state='normal')
    
    def update_status(self, icon, text):
        """Обновляет статус экспорта."""
        self.status_icon.config(text=icon)
        self.status_label.config(text=text)