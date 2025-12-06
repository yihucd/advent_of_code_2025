import collections
import math
import os
import re

demo_mode = int(os.getenv('demo'))

def get_lines(filename):
    demo_filename = 'demo.txt'
    try:
        if not demo_mode:
            with open(filename, 'r') as file:
                lines = [line.strip() for line in file]
        else:
            with open(demo_filename, 'r') as file:
                lines = [line.strip() for line in file]
        
        return lines
    except Exception as e:
        print(f'File read operation exception happened. See details: {e}')
        return []
    
def get_content(filename):
    demo_filename = 'demo.txt'

    try:
        if not demo_mode:
            with open(filename, 'r') as file:
                content = file.read()
        else:
            with open(demo_filename, 'r') as file:
                content = file.read()        
        return content
    except Exception as e:
        print(f'file reading error. See details {e}')

def get_numbers_ops(content):
    """Split the file into 2 parts: number part & operator part."""
    pattern = r'(([0-9 ]+\n)+)([+* ]+)'
    match = re.match(pattern, content)
    if match:
        numbers = match.group(1)
        ops = match.group(3)
    else:
        numbers = ''
        ops = ''

    return (numbers, ops)

def get_op_list(ops_str):
    return [op for op in ops_str.split()]

def get_number_matrix(numbers_str):
    """Get number matrix which has number and space chars in it."""
    lines = [line for line in numbers_str.strip().split('\n')]
    matrix = []
    for line in lines:
        matrix.append([c for c in line])

    return matrix

def get_vertical_column_strs(matrix):
    """Get vertical string in each column."""
    strs_by_column = []

    for col in range(len(matrix[0])):
        col_char_list = []
        for row in range(len(matrix)):
            col_char_list.append(matrix[row][col])
        
        strs_by_column.append(''.join(col_char_list))

    return strs_by_column

def group_vertical_numbers(strs_by_column, num_rows):
    """Group vertical numbers that needs to be operated on together.

    Args:
        strs_by_column (list): A list of strings for each 'thin' column.
        num_rows (int): Number of rows these numbers occupy.
    Returns:
        A dictionary of grouped lists of numbers by column.
    """
    group_count = 0
    column_number_dict = collections.defaultdict(list)  # Key: a number Value: The number to be operated on
    
    for str_by_column in strs_by_column:
        if str_by_column == ' ' * num_rows:  # Found a space separator
            group_count += 1
            continue
        else:
            stripped_str = str_by_column.strip()
            if stripped_str != '':
                number_by_column = int(str_by_column)
                column_number_dict[group_count].append(number_by_column)

    return column_number_dict

content = get_content('day6.txt')
numbers_str, ops_str = get_numbers_ops(content)
number_matrix = get_number_matrix(numbers_str)
vertical_column_strs = get_vertical_column_strs(number_matrix)
num_rows = len(number_matrix)
numbers_by_column = group_vertical_numbers(vertical_column_strs, num_rows)
op_list = get_op_list(ops_str)
total = 0

for i in range(len(op_list)):
    op = op_list[i]
    op_result = 0
    numbers = numbers_by_column[i]
    if op == '+':
        op_result = sum(numbers)
    elif op == '*':
        op_result = math.prod(numbers)
    total += op_result
print(f'total = {total}')
    
