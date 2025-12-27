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

def get_fresh_ranges_and_ids(content):
    """Get ID ranges for fresh items and a list of IDs."""
    fresh_pattern = r'((\d+-\d+\n)+)((\n\d+)+)'
    match = re.match(fresh_pattern, content.strip())

    if match:
        fresh_ranges_str = match.group(1)
        ids_str = match.group(3)
    else:
        fresh_ranges_str = ''
        ids_str = ''

    fresh_id_range_strs = [s.split('-') for s in fresh_ranges_str.split()]
    fresh_id_ranges = []
    for fresh_id_range_str_list in fresh_id_range_strs:
        start = int(fresh_id_range_str_list[0])
        end = int(fresh_id_range_str_list[1])
        fresh_id_ranges.append([start, end])

    ids = [int(s) for s in ids_str.split()]

    return (fresh_id_ranges, ids)

def merge_intervals(fresh_id_ranges):
    """Merge fresh id ranges."""
    if not fresh_id_ranges:
        return []
    
    fresh_id_ranges.sort(key=lambda x: x[0])
    merged = [fresh_id_ranges[0]] 

    for i in range(1, len(fresh_id_ranges)):
        id_range = fresh_id_ranges[i]
        if merged[-1][1] < id_range[0]:
            merged.append(id_range)
        else:
            merged[-1][1] = max(merged[-1][1], id_range[1])

    return merged

def count_fresh_ids(merged_intervals):
    id_count = 0

    for interval in merged_intervals:
        start, end = interval
        id_count += end - start + 1

    return id_count

content = get_content('day5.txt')
fresh_id_ranges, ids = get_fresh_ranges_and_ids(content)
merged_intervals = merge_intervals(fresh_id_ranges)
total_fresh_ingredient_ids = count_fresh_ids(merged_intervals)
print(f'Number of fresh ingredients: {total_fresh_ingredient_ids}')

