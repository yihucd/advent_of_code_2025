import collections
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

lines = get_lines('day7.txt')
matrix = get_matrix(lines)
start = get_starting_node(matrix)
beams, split_times = bfs(matrix, start)
print(f'number of times the beam is splitted = {split_times}')