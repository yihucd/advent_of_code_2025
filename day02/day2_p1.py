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

def get_invalid_id_sum(data_range):
    """Get invalid id count from a range like (11, 22)."""
    invalid_id_sum = 0
    start, end = data_range
    for num in range(start, end + 1):
        num_str = str(num)
        mid = len(num_str) // 2
        left, right = num_str[:mid], num_str[mid:]
        if left == right:
            invalid_id_sum += num

    return invalid_id_sum

line = get_content('day2.txt')
data_ranges = get_data_ranges(line)
total_invalid_id_sum = 0
for data_range in data_ranges:
    total_invalid_id_sum += get_invalid_id_sum(data_range)
print(f'total_invalid_id_sum = {total_invalid_id_sum}')

    