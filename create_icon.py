#!/usr/bin/env python3
"""Создание иконки из изображения."""

import os
import glob
from PIL import Image

# Находим PNG файл с ChatGPT в названии
png_files = glob.glob('ChatGPT*.png')
if not png_files:
    # Пробуем найти любой PNG
    png_files = glob.glob('*.png')

print(f"Найдено файлов: {png_files}")

if png_files:
    png_path = png_files[0]
    print(f"Работаем с: {png_path}")

    img = Image.open(png_path)
    print(f"Исходный размер: {img.size}")
    print(f"Режим: {img.mode}")

    # Конвертируем если нужно
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Создаем ICO - просто сохраняем изображение в формате ICO
    ico_path = 'geodezia.ico'
    img.save(ico_path, format='ICO')
    print(f"\nСоздано: {ico_path}")
    print(f"Размер: {os.path.getsize(ico_path)} bytes")
else:
    print("PNG файлы не найдены!")
    print("Файлы в директории:")
    for f in os.listdir('.'):
        print(f"  {f}")
