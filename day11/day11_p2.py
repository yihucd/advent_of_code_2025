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

@cache
def get_path_count(start, end, adj_list):
    """Calculate the number of paths from start to end node."""
    if start == end:
        return 1
    
    total_path_count = 0
    if start in adj_list:
        for neighbor in adj_list[start]:
            total_path_count += get_path_count(neighbor, end, adj_list)

    return total_path_count

def main():
    lines = get_lines('day11.txt')
    adj_list = get_device_connections(lines)

    path_svr_fft = get_path_count('svr', 'fft', adj_list)
    path_fft_dac = get_path_count('fft', 'dac', adj_list)
    path_dac_out = get_path_count('dac', 'out', adj_list)
    path_svr_fft_dac_out = path_svr_fft * path_fft_dac * path_dac_out

    path_svr_dac = get_path_count('svr', 'dac', adj_list)
    path_dac_fft = get_path_count('dac', 'fft', adj_list)
    path_fft_out = get_path_count('fft', 'out', adj_list)
    path_svr_dac_fft_out = path_svr_dac * path_dac_fft * path_fft_out

    total_paths = path_svr_fft_dac_out + path_svr_dac_fft_out
    print(f'total number of paths from svr to out that pass fft and dac = {total_paths}')

if __name__ == '__main__':
    main()