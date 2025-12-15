import collections
from functools import cache
from frozendict import frozendict
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
    
def get_device_connections(lines):
    """Create adjcency list from the input lines."""
    adj_list = collections.defaultdict(list)

    for line in lines:
        node_str, adj_nodes_str = line.split(':')
        node = node_str.strip()
        adj_nodes = adj_nodes_str.split()
    
        adj_node_tuple = tuple(adj_nodes)
        adj_list[node] = adj_node_tuple

    adj_list_frozen = frozendict(adj_list)

    return adj_list_frozen

# First approach: Use DFS
def get_all_paths_dfs(start, end, adj_list):
    """Use DFS to find all paths."""
    stack = [(start, start)]  # (curr, parent)
    path_count = 0

    while stack:
        curr = stack.pop()
        node, parent = curr

        # Found the end node
        if node == end:
            path_count += 1

        if node in adj_list:        
            for neighbor in adj_list[node]:
                stack.append((neighbor, parent))
    
    return path_count

# Second approach: top-down dynamic programming
# Recursion with memoization
@cache
def get_path_count(start, end, adj_list):
    """Calculate the number of paths from start to end node."""
    if start == end:
        return 1
    
    total_path_count = 0
    for neighbor in adj_list[start]:
        total_path_count += get_path_count(neighbor, end, adj_list)

    return total_path_count

def main():
    lines = get_lines('day11.txt')
    adj_list = get_device_connections(lines)

    # Approach 1: dynamic programming
    path_count = get_path_count('you', 'out', adj_list)

    # Approach 2: DFS
    path_count = get_all_paths_dfs('you', 'out', adj_list)
    
    print(f'path count from "you" to "out" is: {path_count}')

if __name__ == '__main__':
    main()