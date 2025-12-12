import collections
import heapq
import math
import os
import random
from shapely.geometry import Polygon, Point, box
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

def is_green_red(node, global_registry, invalid_registry, boundary_nodes, max_width, max_height):
    """Check if the node is green or red.
    
    Args:
        node (list): A node, e.g., (width, height).
        global_registry (set): If the node is red/green, put in the global registry, i.e., set.
        invalid_registry (set): Registry for node not red/green.
        boundary_nodes (set): All boundary nodes each of which is between two red tiles.
        max_width (int): Max possible width of a node.
        max_height (int): Max possible height of a node.
    Returns:
        None.
    """
    if node in global_registry:
        return True
    
    if node in invalid_registry:
        return False
    
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]] # N, E, S, W

    queue = collections.deque([node])
    seen = {node}
    red_green = True

    while queue:
        curr_node = queue.popleft()
        for d in directions:
            n_w, n_h = curr_node[0] + d[0], curr_node[1] + d[1]
            neighbor = n_w, n_h
            # Case 1: going outside of matrix
            # So the starting node must not be red or green
            if not is_valid(n_w, n_h, max_width, max_height):
                red_green = False
                break
            # Case 2: Hit a red or green boundary nodes:
            elif neighbor in boundary_nodes:
                continue
            # Case 3: contine explore until hitting all nodes within the boundary
            else:
                if neighbor not in seen:
                    queue.append(neighbor)
                    seen.add(neighbor)
    
    # If the node is a red or green node, then it means all nodes seen is also red or green
    if red_green:
        global_registry.update(seen)
        return True
    else:
        seen.remove(node) # remove staring node and not adding it to invalid registry
        invalid_registry.update(seen)
        return False


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

def find_boundary_tiles(nodes):
    """Find all boundary tiles. These are tiles on the boundary of a closed area.

    Args:
        nodes (list): A list of input red nodes.

    Returns:
        A set of boundary tiles each of which is like (width, height).
    """
    boundary_nodes = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1 = nodes[i]
            node2 = nodes[j]
            nodes_on_same_line = find_nodes_on_same_line(node1, node2)
            boundary_nodes.extend(nodes_on_same_line)
    
    return set(boundary_nodes)

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

def is_node_within_pologon_ray_tracing(node, boundary_nodes):
    direction = [-1, 0]  # left
    border_nodes_touched = set()

    # Try to go horizontally to touch a border node 
    stack = [node]
    seen = set([node])

    while stack:
        curr_node = stack.pop()

        if curr_node in boundary_nodes:
            border_nodes_touched.add(curr_node)  

        # Calculate neighbor node
        n_w, n_h = curr_node[0] + direction[0], curr_node[1] + direction[1]
        neighbor = n_w, n_h      

        if is_valid(n_w, n_h, max_width, max_height) and neighbor not in seen:
            stack.append(neighbor)
            seen.add(neighbor)
    
    return border_nodes_touched

def get_two_horizontal_border_nodes(node, boundary_nodes):
    """Get two border nodes left and right.
    
    Args:
        node (tuple): A node like (width, height)
        boundary_nodes: All boundary nodes of red and green color.

    Returns:
        Nodes touching the boundary nodes. Please be noted that
        these are not the boundary nodes themselves. They just touch these
        boundary nodes.
    """
    horizontal_directions = [[-1, 0], [1, 0]]  # left, right
    border_nodes_touched = set()

    # Try to go horizontally to touch a border node 
    stack = [node]
    seen = set([node])

    while stack:
        curr_node = stack.pop()

        for d in horizontal_directions:
            n_w, n_h = curr_node[0] + d[0], curr_node[1] + d[1]
            neighbor = n_w, n_h

            # Case 1: horizontal neighbor node is not within a closed boundary
            # Neighbor node is outside of the matrix
            if not is_valid(n_w, n_h, max_width, max_height):
                return border_nodes_touched
            
            # Case 2: Found a border node horizontally
            elif neighbor in boundary_nodes:
                border_nodes_touched.add(curr_node)  # ****Note: this is the border node, not boundary node

            # Case 3: Not touching boundary node, continue to explore
            elif neighbor not in seen:
                stack.append(neighbor)
                seen.add(neighbor)
    
    return border_nodes_touched

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

def is_area_with_red_green_nodes_only(node1, 
                                      node2, 
                                      max_width, 
                                      max_height, 
                                      global_registry,
                                      invalid_registry,
                                      boundary_nodes):
    """Traverse an area marked by two opposite nodes.
    
    Args:
        node1 (tuple): A node like (width, height) of one corner of the area.
        node2 (tuple): A node like (width, height) of the opposite corner of the area.
        max_width (int): Max value allowed for width.
        max_height (int): Max value allowed for height.
        global_registry (set): A set of red or green nodes.
        invalid_registry (set): A set of nodes not red/green.
        boundary_nodes (set): A set of red or green nodes on the boundaries. 

    Returns:
        True if the area is filled with red and green tiles only.
        False, otherwise.
    """
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]] # N, E, S, W
    stack = [node1]  # Stack for DFS, push one input node into the stack
    seen = {node1}
    area = (node1, node2)
    
    while stack:
        width, height = stack.pop()
        curr_node = width, height
        if not is_green_red(curr_node, global_registry, invalid_registry, boundary_nodes, max_width, max_height):
            return False
        
        for d in directions:
            n_width, n_height = width + d[0], height + d[1]
            neighbor = (n_width, n_height)
            if (is_valid(n_width, n_height, max_width, max_height)
                and is_in_area(area, neighbor)):
                if neighbor not in seen:
                    stack.append(neighbor)
                    seen.add(neighbor)
    
    return True

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
    

def find_largest_area_with_condition0(area_max_heap, max_width, max_height, global_registry, invalid_registry, boundary_nodes, prepared_polygon, polygon):
    """Find the largest area containing only red or green nodes.
    
    Args:
        area_max_heap (list): A max heap based on area sizes. A element on heap is like (area, (node1, node2)).
        max_width (int): Max width of the matrix.
        max_height (int): Max height of the matrix.
        global_registry (set): A set of red/green nodes.
        invalid_registry (set): A set of nodes not red/green.
        boundary_nodes (set): A set of red/green nodes on the bounaries.
        prepared_polygon (PreparedPolygon): A prepared polygon of red nodes.
        polygon (Polygon): A polygon of red nodes.
    """
    max_area = 0
    max_area_nodes = []
    count = 0
    invalid_nodes = set()
    while area_max_heap:
            area_size, (node1, node2) = heapq.heappop(area_max_heap)
            
            # Found the max area, no need to get next element from the max heap
            if max_area >= -area_size:
                break
            
            min_w, min_h, max_w, max_h = nodes_min_max((node1, node2))
            rectangle = box(min_w, min_h, max_w, max_h)
            if rectangle.within(polygon):
                print(f'valid area - node1={node1}, node2={node2}')
                max_area = max(max_area, cal_area(node1, node2))
                max_area_nodes.extend([node1, node2])
    
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

def construct_collision_check_seq(nodes):
    """Construct the list of boxes to check for collisions.
    
    Args:
        nodes: A list of input nodes each of which is like (width, height)

    Returns: 
        A list of boxes to check if the box is a valid box, i.e., box with only red/green nodes in it.
        Each box is represented by a pair of opposite nodes, like [(1, 10), (7, 5)].
    """
    # Create a list of boxes
    box_list = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1 = nodes[i]
            node2 = nodes[j]
            box = (node1, node2)
            box_list.append(box)

    # Create box pairs
    box_pairs = []
    counter = 0
    for i in range(len(box_list)):
        for j in range(i + 1, len(box_list)):
            box1 = box_list[i]
            box2 = box_list[j]
            box_pair = (box1, box2)
            box_pairs.append(box_pair)
            counter += 1
            print(f'count={counter}')

    box_map = collections.defaultdict(list)  # Key: box, Value: a list of boxes colliding with it
    for box in box_list:
        box_map[box].append(box)

    # Pair-wise collision check and update box_map for collision info
    for box_pair in box_pairs:
        box1, box2 = box_pair
        collision = aabb_detection(box1, box2)
        if collision:
            box_map[box1].append(box2)
            box_map[box2].append(box1)
    
    # Use max heap to find out which box to be checked first 
    # on whether the box is a valid box (containing only red/gree nodes).
    max_heap = []
    for box_list in box_map.values():
        heapq.heappush(max_heap, (-len(box_list), box_list))
    
    box_seq = []
    seen = set()

    while max_heap:
        _, box_list = heapq.heappop(max_heap)
        for box in box_list:
            if box not in seen:
                box_seq.append(box)
                seen.add(box)
    
    return box_seq

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

# red_tile_nodes, matrix = gen_matrix(10, 10, 20)
# red_tile_nodes = list(red_tile_nodes)
# print(red_tile_nodes)

lines = get_lines('day9.txt')
red_tile_nodes = get_nodes(lines)
max_width, max_height = get_matrix_width_height(red_tile_nodes)
boundary_nodes = find_boundary_tiles(red_tile_nodes)
polygon = Polygon(red_tile_nodes)
prepared_polygon = prep(polygon)

global_registry = set(boundary_nodes)
invalid_registry = set()

area_max_heap = gen_area_max_heap(red_tile_nodes)
max_area, max_area_nodes = find_largest_area_with_condition0(area_max_heap, max_width, max_height, global_registry, invalid_registry, boundary_nodes, prepared_polygon, polygon)
print(f'The largest area is {max_area}, nodes: {max_area_nodes}')

    




            
