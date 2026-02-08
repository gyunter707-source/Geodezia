#!/usr/bin/env python3
"""Тест для проверки исправления формирования groups"""

import sys
sys.path.insert(0, '.')

from utils.txt_parser import parse_txt, extract_group


def simulate_screen2_logic(txt_data):
    """Симулирует логику Screen2Format.analyze_groups()"""
    if not txt_data:
        return []
    
    # Устанавливаем маппинг колонок
    column_mapping = {'X': 1, 'Y': 2, 'Z': 3}
    
    # Анализируем группы
    groups = {}
    
    for row in txt_data:
        name = row['name']
        group = extract_group(name)
        
        if group:
            if group not in groups:
                groups[group] = {
                    'original': group,
                    'merged': group,
                    'points': []
                }
            groups[group]['points'].append(row)
    
    # Преобразуем в список
    groups_list = list(groups.values())
    return groups_list


# Тест с данными из sample.txt
print("=== ТЕСТ ФОРМИРОВАНИЯ GROUPS ===")

data = parse_txt('data/sample.txt')
print(f"Загружено {len(data)} строк из файла")

groups = simulate_screen2_logic(data)
print(f"Найдено {len(groups)} уникальных групп:")
for g in groups:
    print(f"  - {g['original']} -> {g['merged']} ({len(g['points'])} точек)")

# Проверяем что groups сформирован правильно
expected_groups = ['K', 'NIZR', 'NIZRIG', 'ST']
actual_groups = [g['original'] for g in groups]

print(f"\n=== ПРОВЕРКА ===")
print(f"Ожидаемые группы: {expected_groups}")
print(f"Фактические группы: {actual_groups}")

if set(actual_groups) == set(expected_groups):
    print("✅ ТЕСТ ПРОЙДЕН: Groups сформированы правильно!")
else:
    missing = set(expected_groups) - set(actual_groups)
    extra = set(actual_groups) - set(expected_groups)
    if missing:
        print(f"❌ Отсутствуют: {missing}")
    if extra:
        print(f"⚠️ Лишние: {extra}")
