import collections
from functools import cache
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

def get_matrix(lines):
    matrix = []
    for line in lines:
        char_list = [c for c in line]
        matrix.append(char_list)

    return matrix

def is_valid(row, col, matrix):
    if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
        return True
    return False

def print_matrix(matrix):
    for line in matrix:
        char_str = ''.join(line)
        print(char_str)

def get_starting_node(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 'S':
                return (row, col)
            
def bfs(matrix, start):
    """Do a BFS traversal and return all beam cells.
    
    Args:
        matrix (list): A list of list of nodes.
        start (tuple): The starting node, i.e., 'S' node. For example, (2, 4).

    Returns:
        A tuple containing beam cells and the number of times the beam is splitted.
    """
    queue = collections.deque([start])
    seen = set([start])
    beams = set([start])
    split_times = 0  # Number of times the beam is splitted

    while queue:
        for i in range(len(queue)):
            curr_node = queue.popleft()
            row, col = curr_node

            # Check if there is a splitter next row
            n_row, n_col = row + 1, col
            neighbor = n_row, n_col
            if is_valid(n_row, n_col, matrix):

                # Case 1: the neighbor is a beam cell
                if matrix[n_row][n_col] != '^':
                    if neighbor not in seen:
                        queue.append(neighbor)
                        seen.add(neighbor)
                        beams.add(neighbor)

                # Case 2: the neighbor is a splitter
                # Then the left node and right node to the split are beam cells
                elif matrix[n_row][n_col] == '^':
                    l_row, l_col = n_row, n_col - 1
                    r_row, r_col = n_row, n_col + 1
                    l_node, r_node = (l_row, l_col), (r_row, r_col)
                    split_times += 1
                    for node in [l_node, r_node]:
                        node_row, node_col = node
                        if is_valid(node_row, node_col, matrix) and node not in seen:
                            queue.append(node)
                            seen.add(node)
                            beams.add(node)

    return beams, split_times

def get_beam_map(beams):
    """Convert list of beams to a hash table - Key: row, Value: list of beams that row."""
    beam_map = collections.defaultdict(list)

    for row, col in beams:
        beam_map[row].append((row, col))

    return beam_map

def find_possible_beams_next_row(matrix, beam):
    """Find all possible beam to go for the next row."""
    row, col = beam

    # There are only 3 possible paths to go down next row, i.e., left, middle, right
    possible_beams = set()

    # Check if there is a splitter next row
    n_row, n_col = row + 1, col
    neighbor = n_row, n_col
    if is_valid(n_row, n_col, matrix):

        # Case 1: the neighbor is a beam cell
        if matrix[n_row][n_col] != '^':
            possible_beams.add(neighbor)

        # Case 2: the neighbor is a splitter
        # Then the left node and right node to the split are beam cells
        elif matrix[n_row][n_col] == '^':
            l_row, l_col = n_row, n_col - 1
            r_row, r_col = n_row, n_col + 1
            l_node, r_node = (l_row, l_col), (r_row, r_col)
            if is_valid(l_row, l_col, matrix):
                possible_beams.add(l_node)
            if is_valid(r_row, r_col, matrix):
                possible_beams.add(r_node)

    return possible_beams

@cache
def get_num_of_timelines(matrix, node):
    """Get the number of timeline based on the starting node."""
    num_rows = len(matrix)
    row, col = node

    # Base case
    if row == num_rows - 1:
        return 1
    
    possible_beams_next_row = find_possible_beams_next_row(matrix, node)
    num_of_timelines = 0
    for beam in possible_beams_next_row:
        num_of_timelines += get_num_of_timelines(matrix, beam)
    
    return num_of_timelines
    
def print_path(beam_path, matrix):
    new_matrix = [row[:] for row in matrix]
    for row, col in beam_path:
        new_matrix[row][col] = '|'
    
    print_matrix(new_matrix)

lines = get_lines('day7.txt')

# Get the matrix and start node location, i.e., (row, col).
matrix = get_matrix(lines)
start = get_starting_node(matrix)

# Perform a BFS search to find all beam nodes and the number of times the beam splits
beams, split_times = bfs(matrix, start)

beam_map = get_beam_map(beams)  # A dictionary of light beams, key: row number, value: beams on the row
all_paths = []  # A list of paths each of which is a list of tuples like (row, col)
curr_path = [start]  # A list of nodes for the current path

tuple_matrix = tuple(tuple(row) for row in matrix)
num_of_timelines = get_num_of_timelines(tuple_matrix, start)

print(f'number of timelines = {num_of_timelines}')
    