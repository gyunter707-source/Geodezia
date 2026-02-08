#!/usr/bin/env python3
"""
Модуль экспорта в DXF файл
"""

import ezdxf
import re


def create_dxf(output_path, points_data, column_mapping, layer_mapping, point_type='CIRCLE'):
    """Создаёт DXF файл с точками, текстом имен и Z-отметками.
    
    Args:
        output_path: Путь к выходному DXF файлу
        points_data: Список словарей с данными точек
        column_mapping: {'X': 0, 'Y': 1, 'Z': 2} - индексы колонок
        layer_mapping: {'K': 'K', 'NIZR': 'NIZR_RIGEL'} - группа → слой
        point_type: 'POINT' или 'CIRCLE'
    """
    try:
        # Проверяем параметры
        if not output_path or not points_data or not column_mapping or not layer_mapping:
            raise ValueError("Недостаточно данных для создания DXF")
        
        if len(column_mapping) != 3 or not all(k in column_mapping for k in ['X', 'Y', 'Z']):
            raise ValueError("Некорректное маппинг координат")
        
        # Создаём новый DXF документ (R2000)
        doc = ezdxf.new('R2000')
        msp = doc.modelspace()
        
        # Создаём слои
        # Основные слои для точек
        for layer_name in set(layer_mapping.values()):
            if layer_name and layer_name.strip():
                clean_layer_name = sanitize_layer_name(layer_name)
                if clean_layer_name and clean_layer_name not in doc.layers:
                    doc.layers.add(clean_layer_name)
        
        # Слои для текста имен (суффикс _NAMES)
        for layer_name in set(layer_mapping.values()):
            if layer_name and layer_name.strip():
                clean_layer_name = sanitize_layer_name(layer_name)
                text_layer_name = f"{clean_layer_name}_NAMES"
                if text_layer_name not in doc.layers:
                    doc.layers.add(text_layer_name)
        
        # Слои для Z-отметок (суффикс _Z)
        for layer_name in set(layer_mapping.values()):
            if layer_name and layer_name.strip():
                clean_layer_name = sanitize_layer_name(layer_name)
                z_layer_name = f"{clean_layer_name}_Z"
                if z_layer_name not in doc.layers:
                    doc.layers.add(z_layer_name)
        
        # Добавляем точки, текст имен и Z-отметки
        valid_points_count = 0
        
        for point in points_data:
            # Проверяем, что у нас достаточно колонок
            if len(point['columns']) <= max(column_mapping.values()):
                continue
            
            # Получаем координаты
            try:
                x = float(point['columns'][column_mapping['X']])
                y = float(point['columns'][column_mapping['Y']])
                z = float(point['columns'][column_mapping['Z']])
            except (ValueError, IndexError, TypeError):
                continue
            
            # Получаем имя точки
            point_name = point['name']
            
            # Определяем группу и соответствующий слой
            group = extract_group(point['name'])
            layer_name = layer_mapping.get(group, group)
            
            # Очищаем имена слоев
            clean_layer = sanitize_layer_name(layer_name) if layer_name else "DEFAULT"
            text_layer = f"{clean_layer}_NAMES"
            z_layer = f"{clean_layer}_Z"
            
            if point_type == 'POINT':
                # Добавляем точку
                try:
                    msp.add_point((x, y, z), dxfattribs={'layer': clean_layer})
                    valid_points_count += 1
                except Exception:
                    continue
            else:  # CIRCLE
                # Добавляем круг с центром в точке
                try:
                    msp.add_circle(
                        center=(x, y), 
                        radius=0.05,
                        dxfattribs={'layer': clean_layer}
                    )
                    # Добавляем точку в центре
                    msp.add_point((x, y, z), dxfattribs={'layer': clean_layer})
                    valid_points_count += 1
                except Exception:
                    continue
            
            # Добавляем текст с именем точки
            try:
                if point_name:
                    # Текст имени точки - расположен чуть выше точки
                    msp.add_text(
                        point_name,
                        dxfattribs={
                            'layer': text_layer,
                            'height': 0.15,  # Высота текста
                            'color': 1,     # Красный цвет для имен
                        }
                    ).set_placement((x, y + 0.2, z), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
            except Exception:
                pass  # Пропускаем ошибки добавления текста
            
            # Добавляем текст с Z-отметкой
            try:
                # Форматируем Z как в исходных данных
                z_str = format_z_value(point['columns'][column_mapping['Z']])
                if z_str:
                    msp.add_text(
                        z_str,
                        dxfattribs={
                            'layer': z_layer,
                            'height': 0.12,  # Чуть меньше чем имена
                            'color': 3,     # Зеленый цвет для Z
                        }
                    ).set_placement((x - 0.2, y, z), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
            except Exception:
                pass  # Пропускаем ошибки добавления Z-текста
        
        # Проверяем, были ли добавлены какие-либо точки
        if valid_points_count == 0:
            raise ValueError("Не удалось добавить ни одной корректной точки в DXF")
        
        # Сохраняем
        doc.saveas(output_path)
        return True
        
    except Exception as e:
        print(f"Ошибка при создании DXF: {e}")
        return False


def format_z_value(z_value):
    """Форматирует Z-значение как в исходных данных."""
    try:
        # Пробуем преобразовать в число и обратно в строку
        if isinstance(z_value, (int, float)):
            return str(z_value)
        else:
            # Убираем лишние пробелы
            z_str = str(z_value).strip()
            # Пробуем проверить, что это число
            float(z_str)
            return z_str
    except (ValueError, TypeError):
        return str(z_value)


def sanitize_layer_name(name):
    """Очищает имя слоя от недопустимых символов."""
    if not name:
        return "DEFAULT"
    
    # Удаляем или заменяем недопустимые символы в именах слоёв AutoCAD
    cleaned = re.sub(r'[^\w\s\-_]', '_', str(name))
    
    # Удаляем лишние пробелы
    cleaned = cleaned.strip()
    
    # Если имя слишком длинное, обрезаем
    if len(cleaned) > 255:
        cleaned = cleaned[:255]
    
    # Если имя пустое после очистки, используем DEFAULT
    if not cleaned:
        return "DEFAULT"
    
    return cleaned


def extract_group(name):
    """Извлекает буквенную часть из имени точки."""
    import re
    match = re.match(r'^([A-Za-z]+)', str(name))
    return match.group(1) if match else str(name) if str(name).isalpha() else ""