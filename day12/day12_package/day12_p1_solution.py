######################################
# Working solution for day 12 part 1
######################################

import numpy as np
import os
import re

demo_mode = int(os.getenv('demo'))

def get_lines(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    demo_filename = 'demo.txt'
    try:
        if not demo_mode:
            with open(current_dir + '/' + filename, 'r') as file:
                lines = [line.strip() for line in file]
        else:
            with open(current_dir + '/' + demo_filename, 'r') as file:
                lines = [line.strip() for line in file]
        
        return lines
    except Exception as e:
        print(f'File read operation exception happened. See details: {e}')
        return []
    
def get_content(filename):
    demo_filename = 'demo.txt'
    current_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        if not demo_mode:
            with open(current_dir + '/' + filename, 'r') as file:
                content = file.read()
        else:
            with open(current_dir + '/' + demo_filename, 'r') as file:
                content = file.read()        
        return content
    except Exception as e:
        print(f'file reading error. See details {e}')

def get_shapes_regions(content):
    """Get shapes and regions from the input file."""
    shape_pattern = r'\d+:\n[#.\n]+'
    region_pattern = r'\d+x\d+:[0-9 ]+'
    shapes = re.findall(shape_pattern, content)
    regions = re.findall(region_pattern, content)
    for i in range(len(shapes)):
        shape_num_look = shapes[i].strip()
        shape_look = shape_num_look.split(':')[1].strip()
        shapes[i] = shape_look

    shape_list = []
    for shape in shapes:
        shape_2d = tuple(tuple(char for char in line) for line in shape.split())
        shape_list.append(shape_2d)

    region_list = []
    for region in regions:
        width, length = tuple(int(x) for x in region.split(':')[0].split('x'))
        present_nums = tuple(int(x) for x in region.split(':')[1].split())
        region_list.append(((width, length), present_nums))
    
    return tuple(shape_list), tuple(region_list)

def can_fit(regions):
    """Check if the presents can fit the region using simple 3x3 square 
    covering method without considering overlap cells."""
    dimension, present_list = regions
    width, height = dimension
    total_num_presents = sum(present_list)
    total_presents_can_fit = (width // 3) * (height // 3)
    if total_presents_can_fit >= total_num_presents:
        return True
    return False

def main():
    content = get_content('day12.txt')

    # shapes example: ((('#', '#', '#'), ('#', '#', '.'), ('#', '#', '.')),
    #                 (('#', '#', '#'), ('#', '#', '.'), ('.', '#', '#')))
    # regions example: (((4, 4), (0, 0, 0, 0, 2, 0)), 
    #                  ((12, 5), (1, 0, 1, 0, 2, 2)))
    shapes, regions = get_shapes_regions(content)

    num_areas_fitting_presents = 0
    for region in regions:
        dimension, presents = region # dimension, i.e., (width, height), example: (4, 4), presents example: (0, 0, 0, 0, 2, 0)
        width, height = dimension
        if can_fit(region):
            num_areas_fitting_presents += 1
    
    print(f'Number of areas fitting all presents for each area: {num_areas_fitting_presents}')

if __name__ == '__main__':
    main()