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

    fresh_id_ranges = [s.split('-') for s in fresh_ranges_str.split()]
    ids = [s for s in ids_str.split()]

    return (fresh_id_ranges, ids)

def get_fresh_id_count(fresh_id_ranges, ids):
    """Get the count of fresh ingredients."""
    fresh_id_count = 0
    fresh_id_set = set()

    for id_str in ids:
        id_int = int(id_str)
        for id_range in fresh_id_ranges:
            start, end = int(id_range[0]), int(id_range[1])
            if start <= id_int <= end: 
                fresh_id_set.add(id_int)

    return len(fresh_id_set)

content = get_content('day5.txt')
fresh_id_ranges, ids = get_fresh_ranges_and_ids(content)
fresh_id_count = get_fresh_id_count(fresh_id_ranges, ids)
print(f'Number of fresh ingredients: {fresh_id_count}')

