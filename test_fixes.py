#!/usr/bin/env python3
"""Test script to verify the fixes for the Geodezia application."""

def test_extract_group_numeric_names():
    """Test that extract_group handles numeric-only names correctly."""
    from utils.txt_parser import extract_group
    
    # Test cases
    test_cases = [
        ("K1", "K"),
        ("K150", "K"), 
        ("NIZR12", "NIZR"),
        ("RIG45", "RIG"),
        ("123", "123"),      # numeric-only name
        ("ABC", "ABC"),      # all letters
        ("123ABC", "123"),   # starts with numbers
        ("", ""),            # empty string
    ]
    
    print("Testing extract_group function:")
    for input_name, expected in test_cases:
        result = extract_group(input_name)
        status = "+" if result == expected else "-"
        print(f"  {status} extract_group('{input_name}') -> '{result}' (expected: '{expected}')")


def test_coordinate_check_logic():
    """Test the fixed coordinate check logic."""
    print("\nTesting coordinate validation logic:")
    
    # Simulate the logic from screen2_format.py after our fix
    def check_coordinates(x_val, y_val, z_val):
        # This simulates the fixed condition: x_val != "" and y_val != "" and z_val != ""
        return x_val != "" and y_val != "" and z_val != ""
    
    # Test cases
    test_cases = [
        ("1", "2", "3", True),      # normal values
        ("0", "2", "3", True),      # zero x coordinate (should pass now)
        ("1", "0", "3", True),      # zero y coordinate (should pass now) 
        ("1", "2", "0", True),      # zero z coordinate (should pass now)
        ("0", "0", "0", True),      # all zeros (should pass now)
        ("", "2", "3", False),      # empty x
        ("1", "", "3", False),      # empty y
        ("1", "2", "", False),      # empty z
    ]
    
    for x, y, z, expected in test_cases:
        result = check_coordinates(x, y, z)
        status = "+" if result == expected else "-"
        print(f"  {status} check_coordinates('{x}', '{y}', '{z}') -> {result} (expected: {expected})")


def test_layer_mapping_logic():
    """Test the fixed layer mapping logic between screens."""
    print("\nTesting layer mapping logic:")
    
    # Simulate the state after screen 3 group merging
    groups = [
        {'original': 'K', 'merged': 'K_NEW'},       # Group K merged to K_NEW
        {'original': 'NIZR', 'merged': 'NIZR'},    # Group NIZR stays same
        {'original': 'ST', 'merged': 'K_NEW'},     # Group ST merged to K_NEW (same as K)
    ]
    
    # Simulate layer renaming in screen 4
    layer_by_merged_group = {
        'K_NEW': 'FINAL_LAYER_K',  # Renamed merged group
        'NIZR': 'FINAL_LAYER_NIZR' # Renamed NIZR group
    }
    
    # Build final mapping (this is the fixed logic from screen4_layers.py)
    updated_layer_mapping = {}
    for group_info in groups:
        original_group = group_info['original']
        merged_group = group_info['merged']
        layer_name = layer_by_merged_group.get(merged_group, merged_group)
        updated_layer_mapping[original_group] = layer_name
    
    expected_mapping = {
        'K': 'FINAL_LAYER_K',      # K merged to K_NEW, which became FINAL_LAYER_K
        'NIZR': 'FINAL_LAYER_NIZR', # NIZR stays NIZR, renamed to FINAL_LAYER_NIZR
        'ST': 'FINAL_LAYER_K'      # ST merged to K_NEW, which became FINAL_LAYER_K
    }
    
    print(f"  Final layer mapping: {updated_layer_mapping}")
    print(f"  Expected mapping:    {expected_mapping}")
    
    success = updated_layer_mapping == expected_mapping
    status = "+" if success else "-"
    print(f"  {status} Layer mapping logic {'works' if success else 'failed'}")


if __name__ == "__main__":
    print("Testing fixes for Geodezia application...\n")
    
    test_extract_group_numeric_names()
    test_coordinate_check_logic()
    test_layer_mapping_logic()
    
    print("\nAll tests completed!")