#!/usr/bin/env python3
"""
Модуль парсинга TXT файла тахеометрической съемки
"""

import csv
import re


def parse_txt(file_path):
    """Парсит TXT файл тахеометрической съемки."""
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        # Читаем как CSV с разделителем запятой
        reader = csv.reader(f)
        for row_num, row in enumerate(reader, 1):
            # Убираем пустые значения в конце
            while row and not row[-1].strip():
                row.pop()
            
            if len(row) >= 4:  # Должно быть минимум 4 колонки (имя, x, y, z)
                # Проверяем, что координаты являются числовыми
                name = row[0].strip() if row else ''
                
                # Проверяем, что x, y, z - числа (если нужно строгое требование)
                try:
                    # Проверяем, что следующие 3 колонки содержат числовые значения
                    x_val = float(row[1]) if len(row) > 1 else None
                    y_val = float(row[2]) if len(row) > 2 else None
                    z_val = float(row[3]) if len(row) > 3 else None
                    
                    data.append({
                        'line_num': row_num,
                        'raw_line': ','.join(row),
                        'columns': row,
                        'name': name
                    })
                except (ValueError, TypeError):
                    # Если координаты не числовые, всё равно добавляем (пользователь решит на 2 экране)
                    data.append({
                        'line_num': row_num,
                        'raw_line': ','.join(row),
                        'columns': row,
                        'name': name
                    })
    
    return data


def extract_group(name):
    """Извлекает буквенную часть из имени точки.
    
    K1 → K
    K150 → K
    NIZR12 → NIZR
    RIG45 → RIG
    123 → 123  # числовые имена остаются как есть
    ABC → ABC
    """
    match = re.match(r'^([A-Za-z]+)', str(name))
    if match:
        return match.group(1)
    else:
        # Если нет букв в начале, возвращаем всё имя как есть (включая числа)
        return str(name)


def validate_txt_content(file_path):
    """Проверяет, является ли файл корректным TXT файлом тахеометрии."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sample_lines = []
            for i, line in enumerate(f):
                if i >= 10:  # Проверяем первые 10 строк
                    break
                line = line.strip()
                if line:
                    parts = [p.strip() for p in line.split(',')]
                    # Проверяем, что в строке хотя бы 4 элемента (имя, x, y, z)
                    non_empty_parts = [p for p in parts if p]
                    if len(non_empty_parts) >= 4:
                        sample_lines.append(line)
            
            # Если нашли хотя бы одну подходящую строку, файл валиден
            return len(sample_lines) > 0
            
    except Exception:
        return False