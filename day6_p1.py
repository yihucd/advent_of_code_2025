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

def get_number_matrix(numbers_str):
    """Convert the number part of the file into a 2d matrix of numbers."""
    matrix = []
    lines = numbers_str.strip().split('\n')
    for line in lines:
        number_list = [int(s) for s in line.split()]
        matrix.append(number_list)
        
    return matrix

def get_op_list(ops_str):
    return [op for op in ops_str.split()]

def get_numbers_by_column(matrix):
    """Group numbers by column."""
    numbers_by_column = []

    for col in range(len(matrix[0])):
        number_list = []
        for row in range(len(matrix)):
            number_list.append(matrix[row][col])
        
        numbers_by_column.append(number_list)

    return numbers_by_column

content = get_content('day6.txt')
numbers_str, ops_str = get_numbers_ops(content)
number_matrix = get_number_matrix(numbers_str)
numbers_by_column = get_numbers_by_column(number_matrix)
op_list = get_op_list(ops_str)
total = 0

for numbers, op in zip(numbers_by_column, op_list):
    op_result = 0
    if op == '+':
        op_result = sum(numbers)
    elif op == '*':
        op_result = math.prod(numbers)
    print(f'op_result = {op_result}')
    total += op_result
print(f'total = {total}')
    
    








