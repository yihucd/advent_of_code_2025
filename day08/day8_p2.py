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

def get_boxes(lines):
    boxes = []
    for line in lines:
        boxes.append([int(number) for number in line.strip().split(',')])
    return boxes

def edge_len(box1, box2):
    """Find the edge length between two nodes/boxes."""
    x1, y1, z1 = box1
    x2, y2, z2 = box2
    node_distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
    return node_distance

def find_edges(boxes):
    """Save all pair-wise edge lengths to a map."""
    edge_map = {}
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            nodes = [boxes[i], boxes[j]]
            nodes.sort()
            nodes_tuple =tuple(tuple(x) for x in nodes)
            edge_map[nodes_tuple] = edge_len(boxes[i], boxes[j])
    
    return edge_map

def print_final_circuits(circuits):
    circuit_set = set()
    for circuit in circuits.values():
        circuit_set.add(frozenset(circuit))

    for i, circuit in enumerate(circuit_set):
        print(f'==========#{i}: {circuit}, number of nodes in it: {len(circuit)}')
    
    print(f'total number of circuits left: {len(circuit_set)}')

def make_connection(boxes, edge_map):
    """Make circuit connections between boxes until they all connected together.
    
    Args:
        boxes (list): A list of nodes each of which is a tuple like (x, y, z).
        edge_map (dict): A dict of pair-wise node distances.
    
    Returns:
        A dict of circuits (Key: node, Value: curcuit).
    """
    # Use a min heap to store edges each of which is like
    # (distance, ((box1, box2))
    min_heap = []
    for node_pair, distance in edge_map.items():
        item = (distance, node_pair)
        heapq.heappush(min_heap, item)

    conn_count = 0
    circuits = {}  # Key: node, Value: circuit, i.e., set of nodes connected
    max_heap = [(-1, (None, None))]  # Use it to find the circuit with most nodes so far
    last_two_connected_nodes = (None, None)
    while min_heap:
        distance, node_pair = heapq.heappop(min_heap)
        node1, node2 = node_pair

        # Case 1: both nodes are already connected
        if node1 in circuits and node2 in circuits:
            if circuits[node1] != circuits[node2]:
                merged_set = circuits[node1] | circuits[node2]
                heapq.heappush(max_heap, (-len(merged_set), (node1, node2)))
                last_two_connected_nodes = (node1, node2)
                for node in merged_set:
                    circuits[node] = merged_set
        # Case 2: node1 is already connected to some other node
        elif node1 in circuits:
            curr_circuit = circuits[node1]
            curr_circuit.add(node2)
            circuits[node2] = curr_circuit
            last_two_connected_nodes = (node1, node2)
        # Case 3: node2 is already connected to some other node
        elif node2 in circuits:
            curr_circuit = circuits[node2]
            curr_circuit.add(node1)
            circuits[node1] = curr_circuit
            last_two_connected_nodes = (node1, node2)
        # Case 4: node1 and node2 are in their own circuit
        # So a new circuit needs to be created to connect them together
        else:
            new_circuit = set([node1, node2])
            heapq.heappush(max_heap, (-len(new_circuit), (node1, node2)))
            last_two_connected_nodes = (node1, node2)
            circuits[node1], circuits[node2] = new_circuit, new_circuit
        
        conn_count += 1
        #last_two_connected_nodes = (node1, node2)

    return circuits, last_two_connected_nodes

def print_circuits(circuits):
    circuit_vals = []
    for circuit in circuits.values():
        circuit_vals.append(circuit)

    circuit_vals.sort(key=lambda x: len(x))
    for val in circuit_vals:
        print(val)  

def get_circuit_sets(circuits):
    circuit_sets = set()
    for circuit in circuits.values():
        circuit_sets.add(frozenset(circuit))
    print('---- circuit sets')
    for circuit in circuit_sets:
        print(circuit)
    return circuit_sets

def mul_top_3_curcuit_sizes(circuits):
    circuit_sets = get_circuit_sets(circuits)
    min_heap = []
    for circuit in circuit_sets:
        heapq.heappush(min_heap, len(circuit))
        if len(min_heap) > 3:
            heapq.heappop(min_heap)
    
    return math.prod(min_heap)

# Get all coordinates of boxes
lines = get_lines('day8.txt')
boxes = get_boxes(lines)

# Calculate the length between boxes
edge_map = find_edges(boxes)

# Make all nodes connected by using shortest edge first
circuits, last_two_connected_nodes = make_connection(boxes, edge_map)

# Find the last two connected nodes
node1, node2 = last_two_connected_nodes
x_node1, x_node2 = node1[0], node2[0]
node_product = x_node1 * x_node2
print_final_circuits(circuits)
print(f'Multiplication of the last two connected nodes x coordinates: {node_product}')
            
