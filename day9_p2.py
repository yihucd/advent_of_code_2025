import heapq
import os
from shapely.geometry import Polygon, box

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

def find_other_two_corner_nodes(node1, node2):
    (w1, h1), (w2, h2) = node1, node2
    node3 = (w1, h2)
    node4 = (w2, h1)

    return node3, node4

def gen_rectangle_max_heap(nodes):
    """Generate max heap based on rectangle area size."""
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
    
def find_largest_rectangle(area_max_heap, polygon):
    """Find the largest rectangle containing only red or green nodes.
    
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

def solution():
    lines = get_lines('day9.txt')
    red_tile_nodes = get_nodes(lines)
    polygon = Polygon(red_tile_nodes)

    rectangle_max_heap = gen_rectangle_max_heap(red_tile_nodes)
    max_area, max_area_nodes = find_largest_rectangle(rectangle_max_heap, polygon)
    print(f'The largest rectangle area is {max_area}, nodes: {max_area_nodes}')

if __name__ == '__main__':
    solution()

    




            
