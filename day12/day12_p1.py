import numpy as np
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
    
def convert_to_matrix(shape):
    """Convert the shape to matrix of 0s and 1s."""
    matrix = []
    for line in shape:
        row = []
        for char in line:
            if char == '#':
                row.append(1)
            else: 
                row.append(0)

        matrix.append(row)
    
    return matrix
    
def rotate(shape_matrix, degree):
    np_matrix = np.array(shape_matrix)
    result_matrix = None

    if degree == 90:
        result_matrix = np.rot90(np_matrix, k=-1)
    elif degree == 180:
        result_matrix = np.rot90(np_matrix, k=-2)
    elif degree == 270:
        result_matrix = np.rot90(np_matrix, k=-3)
    
    return result_matrix.tolist()  

def get_region_matrix(region_config):
    width, length = region_config
    return [['.' for w in range(width)] for l in range(length)]

def is_valid(num_rows, num_cols, cell):
    row, col = cell
    if 0 <= row <= num_rows and 0 <= col <= num_cols:
        return True
    return False

def can_fit(start_cell, num_rows, num_cols, empty_cells, shape):
    r_start_cell, c_start_cell = start_cell
    num_rows_shape, num_cols_shape = len(shape), len(shape[0])
    cells_to_be_occupied = set()

    for row in range(num_rows_shape):
        for col in range(num_cols_shape):
            n_row, n_col = r_start_cell + row, c_start_cell + col
            new_cell = n_row, n_col
            if not is_valid(num_rows, num_cols, new_cell):
                return (False, None)
            else:
                if not new_cell in empty_cells:
                    return (False, None)
                cells_to_be_occupied.add(new_cell)

    return (True, cells_to_be_occupied)

def add_newly_used_cells(used_cells, start_cell, shape):
    """Add newly used cells."""
    s_row, s_col = start_cell
    occupied_cells = set()

    for row in range(len(shape)):
        for col in range(len(shape[0])):
            occupied_cell = s_row + row, s_col + col
            occupied_cells.add(occupied_cell)
    
    used_cells |= occupied_cells

def remove_newly_used_cells(used_cells, start_cell, shape):
    """Remove newly used cells."""
    s_row, s_col = start_cell
    occupied_cells = set()

    for row in range(len(shape)):
        for col in range(len(shape[0])):
            occupied_cell = s_row + row, s_col + col
            occupied_cells.add(occupied_cell)
    
    used_cells -= occupied_cells

global_counter = 0

def backtrack(width, height, presents, curr_presents, all_cells, shapes, used_cells):
    """Use backtrack to see if all shapes can fit.
    
    Args:
        width (int): The width of the area for placing presents.
        height (int): The height of the area for placing presents.
        presents (list): The list of presents to be placed in the area.
        curr_presents (list): The current list of presents already placed in the area.
        all_cells (list): The 2D list of cells each of which is a tuple (row, col).
        shapes (list): The list of shapes each of which is a matrix.
        used_cells (list): The list of already used cells each of which is a tuple (row, col).

    Returns:
        bool: True if all presents can fit in the area, False otherwise.
    """
    global global_counter 
    global_counter += 1
    print(f'global_counter={global_counter}')
    print(f'presents={presents}')
    print(f'curr_presents={curr_presents}')

    if set(presents) == set(curr_presents):
        return True
    
    presents_left = [total - placed for total, placed in zip(presents, curr_presents)]
    num_rows, num_cols = height, width 
    empty_cells = all_cells - used_cells
    rotate_degrees = [90, 180, 270]

    for start_cell in empty_cells:
        for i, num_presents in enumerate(presents_left):
            for j in range(num_presents):
                for degree in rotate_degrees:
                    curr_shape = rotate(shapes[i], degree) 
                    if can_fit(start_cell, num_rows, num_cols, empty_cells, curr_shape):
                        curr_presents[i] += 1
                        add_newly_used_cells(used_cells, start_cell, curr_shape)
                        if backtrack(width, height, presents, curr_presents, all_cells, shapes, used_cells):
                            return True
                        remove_newly_used_cells(used_cells, start_cell, curr_shape)
                        curr_presents[i] -= 1

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
        num_rows, num_cols = height, width
        all_cells = set([(row, col) for row in range(num_rows) for col in range(num_cols)])
        curr_presents = [0 for i in range(len(presents))]
        used_cells = set()
        can_fit_presents = backtrack(width, height, presents, curr_presents, all_cells, shapes, used_cells)
        if can_fit_presents:
            num_areas_fitting_presents += 1
    
    print(f'Number of areas fitting all presents for each area: {num_areas_fitting_presents}')

if __name__ == '__main__':
    main()