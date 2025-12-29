##########################################
# Backtrack solution for day 12 part 1.
# This solution seems to be working for small size input (not for large size input).
# It was not fully tested though.
##########################################

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
    
    result_matrix = result_matrix.tolist()
    result_tuple = tuple(tuple(row) for row in result_matrix)
    return result_tuple

def get_region_matrix(region_config):
    width, length = region_config
    return [['.' for w in range(width)] for l in range(length)]

def is_valid(num_rows, num_cols, cell):
    row, col = cell
    if 0 <= row < num_rows and 0 <= col < num_cols:
        return True
    return False

def can_fit(start_cell, num_rows, num_cols, empty_cells, shape):
    """Check if the shape can fit in the area's empty cells."""
    r_start_cell, c_start_cell = start_cell
    num_rows_shape, num_cols_shape = len(shape), len(shape[0])
    cells_to_be_occupied = set()

    for row in range(num_rows_shape):
        for col in range(num_cols_shape):
            n_row, n_col = r_start_cell + row, c_start_cell + col
            new_cell = n_row, n_col
            if shape[row][col] == '.':  # Not used
                continue

            if not is_valid(num_rows, num_cols, new_cell):
                return False
            else:
                if not new_cell in empty_cells:
                    return False
                cells_to_be_occupied.add(new_cell)

    return True

def add_newly_used_cells(used_cells, start_cell, shape):
    """Add newly used cells."""
    s_row, s_col = start_cell
    occupied_cells = set()

    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col] == '#':
                occupied_cell = s_row + row, s_col + col
                occupied_cells.add(occupied_cell)
    
    used_cells |= occupied_cells

def set_test(input_set):
    tmp_set = {5, 9}
    input_set |= tmp_set

def remove_newly_used_cells(used_cells, start_cell, shape):
    """Remove newly used cells."""
    s_row, s_col = start_cell
    occupied_cells = set()

    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col] == '#':
                occupied_cell = s_row + row, s_col + col
                occupied_cells.add(occupied_cell)
    
    used_cells -= occupied_cells

global_counter = 0

def get_width_height_empty_area(empty_area):
    rows, cols = set(), set()
    for row, col in empty_area:
        rows.add(row)
        cols.add(col)
    width, height = len(cols), len(rows)
    return width, height

def empty_cells_possily_fit(width, height, all_cells, used_cells, shape):
    """From all empty cells, find out possible empty cells that possily fit the shape."""
    selected_cells_to_try = set()
    num_rows, num_cols = height, width
    shape_square_length = max(len(shape), len(shape[0]))
    seen = set()
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    for cell in all_cells:
        if cell not in seen:
            stack = [cell]
            empty_area = set()

            # Find cells in each empty area
            while stack:
                curr = stack.pop()
                row, col = curr
                for d in directions:
                    n_row, n_col = row + d[0], col + d[1]
                    neighbor = n_row, n_col
                    if is_valid(num_rows, num_cols, neighbor):
                        if neighbor not in used_cells and neighbor not in seen:
                            empty_area.add(neighbor)
                            stack.append(neighbor)
                            seen.add(neighbor)

            # Find if the empty area is big enoughf for the shape
            shape_width = len(shape[0])
            shape_height = len(shape)
            min_shape_width_height = min(shape_width, shape_height)
            shape_size = len(shape) * len(shape[0])
            area_width, area_height = get_width_height_empty_area(empty_area)
            if (len(empty_area) >= shape_size and 
                area_width >= shape_width and 
                area_height >= shape_height):
                selected_cells_to_try |= empty_area

    # Find out if the empty cell is too far away
    max_row, max_col = 0, 0
    final_selection = set()
    for cell in used_cells:
        row, col = cell
        max_row = max(max_row, row)
        max_col = max(max_col, col)

    for cell in selected_cells_to_try:
        row, col = cell
        if not (row - max_row > shape_square_length and 
            col - max_col > shape_square_length):    
            final_selection.add(cell)

    return final_selection

def empty_cells_possily_fit_with_rotate(width, height, all_cells, used_cells, shapes):
    degrees = [90, 180, 270]
    cells_map = {}
    for shape in shapes:
        for degree in degrees:
            curr_shape = rotate(shape, degree)
            cells_to_be_considered = empty_cells_possily_fit(width, height, all_cells, used_cells, curr_shape)
            cells_map[(shape, degree)] = cells_to_be_considered

    return cells_map

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

    if presents == tuple(curr_presents):
        return True
    
    presents_left = [total - placed for total, placed in zip(presents, curr_presents)]
    num_rows, num_cols = height, width 
    empty_cells = list(all_cells - used_cells)
    empty_cells.sort()
    
    print(f'number of empty cells = {len(empty_cells)}')
    possible_cells_to_fit_map = empty_cells_possily_fit_with_rotate(width, height, all_cells, used_cells, shapes)
    print(f'possible cells to fit - 90: {len(possible_cells_to_fit_map[(shapes[0], 90)])}')

    rotate_degrees = [90, 180, 270]
    for start_cell in empty_cells:
        for i, num_presents in enumerate(presents_left):
            for j in range(num_presents):
                for degree in rotate_degrees:
                    curr_shape = rotate(shapes[i], degree)
                    if not possible_cells_to_fit_map[(shapes[i],degree)]:
                        return False
                    if can_fit(start_cell, num_rows, num_cols, possible_cells_to_fit_map[(shapes[i],degree)], curr_shape):
                        curr_presents[i] += 1
                        add_newly_used_cells(used_cells, start_cell, curr_shape)
                        display_cells(width, height, used_cells)  # show the area in color
                        if backtrack(width, height, presents, curr_presents, all_cells, shapes, used_cells):
                            return True
                        remove_newly_used_cells(used_cells, start_cell, curr_shape)
                        curr_presents[i] -= 1

    return False

def print_color_str(input, color):
    color_dict = {
        'red': '\033[91m',
        'green': '\033[92m',
    }
    start_color = color_dict[color]
    end_color = '\033[0m'  # The essential code to reset formatting back to default

    print(f"{start_color}{input}{end_color}", end='')

def print_matrix(matrix):
    print('  ', end='')
    for col in range(len(matrix[0])):
        print(f'{col:>2}', end='')
    print()
    for row in range(len(matrix)):
        for col in range(len(matrix[0]) + 1):
            if col == 0:
                print(f'{row:>2} ', end='')
            
            if col == len(matrix[0]):
                print(f'{row:<2} ', end='')
                break

            if matrix[row][col] == '.':
                print('. ', end='')
            elif matrix[row][col] == '#':
                print_color_str('# ', 'red')
            elif matrix[row][col] == 'X':
                print_color_str('X ', 'green')
        print()
    
    print('  ', end='')
    for col in range(len(matrix[0])):
        print(f'{col:>2}', end='')
    print()

def display_cells(width, height, used_cells):
    num_rows, num_cols = height, width 
    for row in range(num_rows):
        for col in range(num_cols):
            cell = row, col
            if cell not in used_cells:
                print_color_str('. ', 'green')
            else:
                print_color_str('# ', 'red')
        print()

def main():
    content = get_content('day12.txt')

    # shapes example: ((('#', '#', '#'), ('#', '#', '.'), ('#', '#', '.')),
    #                 (('#', '#', '#'), ('#', '#', '.'), ('.', '#', '#')))
    # regions example: (((4, 4), (0, 0, 0, 0, 2, 0)), 
    #                  ((12, 5), (1, 0, 1, 0, 2, 2)))
    shapes, regions = get_shapes_regions(content)

    shape0 = shapes[0]
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