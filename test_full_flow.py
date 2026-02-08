#!/usr/bin/env python3
"""Полный тест flow приложения"""

import sys
sys.path.insert(0, '.')

from utils.txt_parser import parse_txt, extract_group


def test_full_flow():
    """Тестирует полный flow от загрузки файла до формирования groups."""
    print("=== ТЕСТ ПОЛНОГО FLOW ===\n")

    # Шаг 1: Загрузка файла (имитирует Screen1Welcome)
    print("Шаг 1: Загрузка файла")
    txt_data = parse_txt('data/sample.txt')
    print(f"  Загружено {len(txt_data)} строк")

    if not txt_data:
        print("  ОШИБКА: Данные не загружены!")
        return False

    # Симулируем state
    state = {
        'txt_data': txt_data,
        'column_mapping': {},
        'groups': [],
    }

    # Шаг 2: Выбор координат (имитирует auto_select_coords из Screen2Format)
    print("\nШаг 2: Автоматический выбор координат")
    first_row = txt_data[0].get('columns', [])

    if len(first_row) < 4:
        print(f"  ОШИБКА: Недостаточно колонок: {first_row}")
        return False

    # Находим 3 числовые колонки
    numeric_cols = []
    for i, val in enumerate(first_row[1:], 1):
        try:
            float(val)
            numeric_cols.append((i, val))
        except ValueError:
            pass

    if len(numeric_cols) >= 3:
        x_idx, x_val = numeric_cols[0]
        y_idx, y_val = numeric_cols[1]
        z_idx, z_val = numeric_cols[2]
        print(f"  X={x_idx}({x_val}), Y={y_idx}({y_val}), Z={z_idx}({z_val})")
    else:
        print("  Используем стандартные индексы 1,2,3")
        x_idx, y_idx, z_idx = 1, 2, 3

    # Устанавливаем маппинг
    state['column_mapping'] = {'X': x_idx, 'Y': y_idx, 'Z': z_idx}

    # Шаг 3: Анализ групп (имитирует analyze_groups из Screen2Format)
    print("\nШаг 3: Анализ групп")

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

    state['groups'] = list(groups.values())
    print(f"  Найдено {len(state['groups'])} групп")

    for g in state['groups']:
        print(f"    - {g['original']} -> {g['merged']} ({len(g['points'])} точек)")

    # Шаг 4: Проверка готовности к экрану 3
    print("\nШаг 4: Проверка готовности к Screen3Groups")
    can_go_next = len(state['groups']) > 0
    print(f"  can_go_next = {can_go_next}")

    if not can_go_next:
        print("  ОШИБКА: Невозможно перейти к экрану 3!")
        return False

    # Шаг 5: Проверка данных для Screen3Groups
    print("\nШаг 5: Данные для Screen3Groups")
    print(f"  state['groups'] = {state['groups']}")

    expected_format = all(
        'original' in g and 'merged' in g
        for g in state['groups']
    )

    if expected_format:
        print("  Формат данных корректен!")
    else:
        print("  ОШИБКА: Неверный формат данных!")
        return False

    print("\n=== ТЕСТ ПРОЙДЕН ===")
    return True


if __name__ == '__main__':
    success = test_full_flow()
    sys.exit(0 if success else 1)
