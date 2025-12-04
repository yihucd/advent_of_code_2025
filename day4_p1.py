import os
import heapq

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

def get_paper_rolls(matrix):
    """Get the locations of all paper rolls that can be accessed by forklifts.
    
    Args:
        matrix (list): A list of list of cell contents.

    Returns:
        The list of locations of paper rolls accessible by forklifts.
    """
    directions = [
        [-1, 0],  # N
        [0, 1],  # E
        [1, 0],  # S
        [0, -1], # W
        [-1, 1], # NE
        [1, 1], # SE
        [1, -1], # SW
        [-1, -1], # NW
    ]

    paper_roll_set = set()
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            neighbor_paper_rolls = set()
            if matrix[r][c] == '@':
                for d in directions:
                    n_r, n_c = r + d[0], c+ d[1]
                    if is_valid(n_r, n_c, matrix) and matrix[n_r][n_c] == '@':
                        neighbor_paper_rolls.add((n_r, n_c))
                
                if len(neighbor_paper_rolls) < 4:
                    paper_roll_set.add((r, c))
    
    return paper_roll_set

lines = get_lines('day4.txt')
matrix = get_matrix(lines)
paper_roll_set = get_paper_rolls(matrix)
print(f'paper roll count is {len(paper_roll_set)}')