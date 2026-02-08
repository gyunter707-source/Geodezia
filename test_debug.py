#!/usr/bin/env python3
"""Test the fix for screen2 coordinate extraction."""

import re

# Симулируем извлечение чисел из примера строки
example_text = "TOCHKA,  15.455,  31.455,  0.540"
numbers = re.findall(r'-?\d+\.?\d*', example_text)

print("=" * 60)
print("TESTING: Extract numbers from example string")
print("=" * 60)
print(f"Example text: '{example_text}'")
print(f"Extracted numbers: {numbers}")

if len(numbers) >= 3:
    example_values = numbers[:3]
    print(f"\nValues for ComboBox: {example_values}")
    print(f"X = {example_values[0]}")
    print(f"Y = {example_values[1]}")
    print(f"Z = {example_values[2]}")

    # Проверяем что все разные
    if len({example_values[0], example_values[1], example_values[2]}) == 3:
        print("\n✅ All values are different - button will be ENABLED")
    else:
        print("\n❌ Some values are equal - button will be DISABLED")
else:
    print(f"\n❌ Could not extract 3 numbers from example")

print("=" * 60)

# Тест с файлом пользователя
print("\nTESTING: User's file data")
print("=" * 60)
user_first_row = ['1', '0.000', '0.000', '0.000']
print(f"First row from file: {user_first_row}")

# Показываем что происходит без исправления
numeric_cols = []
for i, val in enumerate(user_first_row[1:], 1):
    try:
        float(val)
        numeric_cols.append((i, val))
    except ValueError:
        pass

print(f"Numeric columns: {numeric_cols}")
if len(numeric_cols) >= 3:
    print(f"OLD behavior - would show: X={numeric_cols[0][1]}, Y={numeric_cols[1][1]}, Z={numeric_cols[2][1]}")
    print("❌ All values are 0.000 - button DISABLED!")
print("=" * 60)
