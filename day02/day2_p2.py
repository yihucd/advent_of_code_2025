import os

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

def get_data_ranges(line):
    """Get data range from input and return a list of tuples of (start, end)."""
    ranges = line.strip().split(',')
    int_ranges = []
    for data_range in ranges:
        start_str, end_str = data_range.split('-')
        start, end = int(start_str), int(end_str)
        int_ranges.append((start, end))
    
    return int_ranges

def split_str_into_parts(input_str, num_parts):
    """Split a string evenly into number of parts specified."""
    input_len = len(input_str)
    if input_len % num_parts != 0:
        return []
    
    parts = []
    part_length = input_len // num_parts
    for i in range(num_parts):
        start_idx = i * part_length
        end_idx = (i + 1) * part_length 
        parts.append(input_str[start_idx: end_idx])

    return parts


def get_invalid_id_sum(data_range):
    """Get invalid id count from a range like (11, 22).
    
    An ID is invalid if it is made only of some sequence of digits repeated at least twice. 
    So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), 
    and 1111111 (1 seven times) are all invalid IDs.
    """
    invalid_id_sum = 0
    start, end = data_range
    for num in range(start, end + 1):
        num_str = str(num)
        num_str_len = len(num_str)
        for num_parts in range(2, num_str_len + 1):
            parts = split_str_into_parts(num_str, num_parts)
            parts_set = set(parts)
            if len(parts_set) == 1:
                invalid_id_sum += num
                break

    return invalid_id_sum

line = get_content('day2.txt')
data_ranges = get_data_ranges(line)
total_invalid_id_sum = 0
for data_range in data_ranges:
    total_invalid_id_sum += get_invalid_id_sum(data_range)
print(f'total_invalid_id_sum = {total_invalid_id_sum}')


    