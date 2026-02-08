#!/usr/bin/env python3
"""Test DXF export."""

import sys
sys.path.insert(0, '.')

from utils.txt_parser import parse_txt
from utils.dxf_exporter import create_dxf

print('Loading data...')
data = parse_txt('data/sample.txt')
print(f'Loaded {len(data)} rows')
print(f'First row: {data[0] if data else None}')

print('Creating DXF...')
try:
    result = create_dxf(
        output_path='test_output.dxf',
        points_data=data,
        column_mapping={'X': 1, 'Y': 2, 'Z': 3},
        layer_mapping={'K': 'K'},
        point_type='CIRCLE'
    )
    print(f'Result: {result}')
except Exception as e:
    print(f'ERROR: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
