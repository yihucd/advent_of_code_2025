import heapq
import os
import random
from shapely.geometry import Polygon, box
from shapely.prepared import prep


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

def get_nodes(lines):
    nodes = []
    for line in lines:
        str_num_list = line.strip().split(',')
        num_list = [int(s) for s in str_num_list]
        nodes.append(tuple(num_list))
    return nodes

def cal_area(node1, node2):
    w1, h1 = node1
    w2, h2 = node2
    area = (abs(w1 - w2) + 1) * (abs(h1 - h2) + 1)
    return area

def is_valid(width, height, max_width, max_height):
    if 0 <= width <= max_width and 0 <= height <= max_height:
        return True
    return False

def get_matrix_width_height(nodes):
    max_width, max_height = 0, 0
    for width, height in nodes:
        max_width = max(max_width, width)
        max_height = max(max_height, height)
    
    return (max_width, max_height)

def is_in_area(area, node):
    """Check if the node is in the rectangle area.
    
    Args:
        area (tuple): A 2-tuple of nodes representing opposite nodes of the rectangle.
        node (tuple): A tuple representation of a node, like (width, height).

    Returns:
        True if the node is in the area. False, otherwise.
    """
    (w1, h1), (w2, h2) = area

    n_w, n_h = node
    return  (min(w1, w2) <= n_w <= max(w1, w2) and min(h1, h2) <= n_h <= max(h1, h2))


def find_nodes_on_same_line(node1, node2):
    """Find all tiles between two nodes that are on a straight line."""
    (w1, h1), (w2, h2) = node1, node2
    result = []

    # Return a empty list of these two nodes are not on a horizontal or vertical line
    if w1 != w2 and h1 != h2:
        return result
    
    if w1 == w2 and h1 != h2:
        result = [(w1, h) for h in range(min(h1, h2), max(h1, h2) + 1)]
        return result
    
    if w1 != w2 and h1 == h2:
        result = [(w, h1) for w in range(min(w1, w2), max(w1, w2) + 1)]
        return result
    
    if w1 == w2 and h1 == h2: # Same node
        result = [(w1, h1)]
        return result

def find_other_two_corner_nodes(node1, node2):
    (w1, h1), (w2, h2) = node1, node2
    node3 = (w1, h2)
    node4 = (w2, h1)

    return node3, node4

def is_node_touching_boundary(node, boundary_nodes):
    ##TODO change the comment for direction
    """Check if a node touch boundary nodes in 8 directions."""
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

    for d in directions:
        n_w, n_h = node[0] + d[0], node[1] + d[1]
        if (n_w, n_h) in boundary_nodes:
            return True
    
    return False

def get_neighbor_nodes_heap(node, boundary_nodes, max_width, max_height):
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]] # left, down, right, up
    min_heap = []
    for d in directions:
        n_w, n_h = node[0] + d[0], node[1] + d[1]
        neighbor = n_w, n_h

        # All neighbor nodes on heap should be valid and not boundary nodes
        if (is_valid(n_w, n_h, max_width, max_height) 
            and neighbor not in boundary_nodes):

            # Priority 0 for neighbor touching the boundary
            if is_node_touching_boundary(neighbor, boundary_nodes):
                heapq.heappush(min_heap, (0, neighbor))
            else:
                heapq.heappush(min_heap, (1, neighbor))
    
    return min_heap

def is_node_within_boundary(node, boundary_nodes, max_width, max_height):
    if node in boundary_nodes:
        return True
    
    horizontal_border_nodes_touched = get_two_horizontal_border_nodes(node, boundary_nodes)

    # Not seen two border nodes, so not within closed boundary
    if len(horizontal_border_nodes_touched) < 2:  
        return False

    # Pick a border node as the start node and start to explore along the boundary nodes
    # Use DFS so we always go along the border
    start_node = list(horizontal_border_nodes_touched)[0]
    stack = [start_node]
    seen = set()

    first_visited_start_node = True
    while stack:
        curr_node = stack.pop()
        seen.add(curr_node)

        # Push start node back to the stack the first time it is visited
        # If we see it again in the future, we know we looped around the closed area
        if curr_node == start_node:
            if first_visited_start_node:
                stack.append(start_node)
                first_visited_start_node = False
            else:
                # Coming back to the start node again, so we have a closed area
                return True

        # Generate a min heap populated with neighbor nodes
        # All of these are valid nodes and not in boundary node
        # Nodes touching boundary will have a priority of 0, others having priority 1
        # Elment on heap is like (0, node), or (1, node)
        min_heap = get_neighbor_nodes_heap(curr_node, boundary_nodes, max_width, max_height)

        unseen_border_nodes = 0
        unseen_nonborder_nodes = 0
        while min_heap:
            distance_to_boundary, neighbor = heapq.heappop(min_heap)
            # Only push nodes on heap touching boundary to the stack
            # Because we want to go around the closed area by following the wall/boundary nodes
            if neighbor not in seen:
                if distance_to_boundary == 0:
                    unseen_border_nodes += 1
                    stack.append(neighbor)
                else:
                    unseen_nonborder_nodes += 1
            
        # If there isn't unseen border nodes from the heap before we get back to the start node,
        # then there isn't a closed area
        if unseen_border_nodes == 0 and unseen_nonborder_nodes > 0:
            return False
        
    return False # This is a bit redundant


def gen_area_max_heap(nodes):
    """Generate max heap based on area size."""
    max_heap = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1 = nodes[i]
            node2 = nodes[j]
            area = cal_area(node1, node2)
            heapq.heappush(max_heap, (-area, (node1, node2)))
    
    return max_heap

def nodes_min_max(nodes):
    (w1, h1), (w2, h2) = nodes

    min_w, max_w = min(w1, w2), max(w1, w2)
    min_h, max_h = min(h1, h2), max(h1, h2)

    return min_w, min_h, max_w, max_h

def is_node_in_a_box(node, box):
    (w1, h1), (w2, h2) = box

    min_w, max_w = min(w1, w2), max(w1, w2)
    min_h, max_h = min(h1, h2), max(h1, h2)

    n_w, n_h = node
    if min_w <= n_w <= max_w and min_h <= n_h <= max_h:
        return True
    return False
    

def find_largest_area(area_max_heap, polygon):
    """Find the largest area containing only red or green nodes.
    
    Args:
        area_max_heap (list): A max heap based on area sizes. A element on heap is like (area, (node1, node2)).
        polygon (Polygon): A polygon of red nodes.
    """
    max_area = 0
    max_area_nodes = []
    while area_max_heap:
            area_size, (node1, node2) = heapq.heappop(area_max_heap)
            min_w, min_h, max_w, max_h = nodes_min_max((node1, node2))
            rectangle = box(min_w, min_h, max_w, max_h)
            if rectangle.within(polygon):
                max_area = max(max_area, -area_size)
                max_area_nodes.extend([node1, node2])
                break
    
    return max_area, max_area_nodes


def aabb_detection(box1, box2):
    """Detect if box 1 and box 2 collide with each other.

    Args:
        box1 (list): Two opposite nodes each of which is like (width, height).
        box2 (list): Two opposite nodes each of which is like (width, height).
    
    Returns:
        True if collide, False otherwise.
    """
    (box1_w1, box1_h1), (box1_w2, box1_h2) = box1
    (box2_w1, box2_h1), (box2_w2, box2_h2) = box2

    box1_min_w, box1_max_w = min(box1_w1, box1_w2), max(box1_w1, box1_w2)
    box1_min_h, box1_max_h = min(box1_h1, box1_h2), max(box1_h1, box1_h2)
    
    box2_min_w, box2_max_w = min(box2_w1, box2_w2), max(box2_w1, box2_w2)
    box2_min_h, box2_max_h = min(box2_h1, box2_h2), max(box2_h1, box2_h2)

    if (box1_min_w <= box2_max_w and
        box1_max_w >= box2_min_w and
        box1_min_h <= box2_max_h and
        box1_max_h >= box2_min_h):
        return True
    return False

def gen_matrix(width, height, num_red_tiles):
    """Generate a matrix based on the number of rows and cols and num of red tiles.
    
    Args:
        width (int): width of the matrix
        height (int): height of the matrix
        num_red_tiles (int): Number of red tiles.
    
    Returns:
        A tuple (node_set, matrix) where node_set is a set of nodes and
        matrix is a 2d matrix where "." is a empty space and "#" is a red tile.
    """
    red_tile_set = set()
    matrix = []

    while True:
        w, h = random.randint(0, width - 1), random.randint(0, height - 1) 
        red_tile_set.add((w, h))
        if len(red_tile_set) == num_red_tiles:
            break

    for h in range(height):
        line = []
        for w in range(width):
            if (w, h) in red_tile_set:
                line.append('#')
            else:
                line.append('.')
        matrix.append(line)

    return red_tile_set, matrix

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

def set_boundary_nodes_to_x(matrix, boundary_nodes, red_tile_nodes):
     for node in boundary_nodes:
         w, h = node
         row, col = h, w
         if (w, h) not in red_tile_nodes:
             matrix[row][col] = 'X'

def solution():
    lines = get_lines('day9.txt')
    red_tile_nodes = get_nodes(lines)
    max_width, max_height = get_matrix_width_height(red_tile_nodes)
    polygon = Polygon(red_tile_nodes)
    prepared_polygon = prep(polygon)

    area_max_heap = gen_area_max_heap(red_tile_nodes)
    max_area, max_area_nodes = find_largest_area(area_max_heap, polygon)
    print(f'The largest area is {max_area}, nodes: {max_area_nodes}')

if __name__ == '__main__':
    solution()

    




            
