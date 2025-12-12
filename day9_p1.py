import heapq
import math
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

def get_nodes(lines):
    nodes = []
    for line in lines:
        str_num_list = line.strip().split(',')
        num_list = [int(s) for s in str_num_list]
        nodes.append(num_list)
    return nodes

def cal_area(node1, node2):
    w1, h1 = node1
    w2, h2 = node2
    area = abs(w1 - w2 + 1) * abs(h1 - h2 + 1)
    return area

def find_largest_area(nodes):
    """Find the largest area between two nodes."""
    max_area = 0
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1 = nodes[i]
            node2 = nodes[j]
            max_area = max(max_area, cal_area(node1, node2))
    
    return max_area

lines = get_lines('day9.txt')
nodes = get_nodes(lines)
largest_area = find_largest_area(nodes)
print(f'The largest area is {largest_area}')



            
