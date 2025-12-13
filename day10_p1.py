from functools import cache
import os
import re
import sys

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

def get_machine_configs(line):
    """Get diagram, buttons, joltages configs from each machine."""
    # Example: [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    pattern = r'\[(.+)\] (.+) (\{.+\})'
    match = re.fullmatch(pattern, line)
    if not match:
        raise RuntimeError(f'Line does not match the expected format: {line}')

    diagram_str = match.group(1)
    buttons_str = match.group(2)
    joltages_str = match.group(3)

    diagram = tuple(light for light in diagram_str)
    buttons = tuple(tuple(int(press) for press in button.strip('()').split(',')) for button in buttons_str.split())
    joltages = tuple(int(joltage) for joltage in joltages_str.strip('{}').split(','))

    return diagram, buttons, joltages

@cache
def find_shortest_seq_presses(machine_configs, curr, prev_buttons):
    """Find the shortest number of presses to get the desired light diagram.
    
    Args:
        machine_configs (tuple): A tuple representing (diagram, buttons, joltages).
        curr (tuple): Curent light config.
        prev_buttons (frozenset): Previous buttons pressed.

    Returns:
        Smallest number of presses to get the desired diagram.
    """
    diagram, buttons, joltages = machine_configs

    # If the current light config is desirable, no need to press any button
    if curr == diagram:
        return 0
    
    if len(prev_buttons) == len(buttons):
        return float('inf')
    
    options = []
    for button in buttons:
        if button in prev_buttons:
            continue

        new_config = list(curr)
        for toggle in button:
            if new_config[toggle] == '.':
                new_config[toggle] = '#'
            else:
                new_config[toggle] = '.'
            
        new_button_set = set(prev_buttons)
        new_button_set.add(button)
        press_number = find_shortest_seq_presses(machine_configs, tuple(new_config), frozenset(new_button_set)) + 1
        options.append(press_number)

    return min(options)

def main():
    lines = get_lines('day10.txt')
    total_num_presses = 0
    
    for i, line in enumerate(lines):
        # Get each machine's configs
        machine_configs = get_machine_configs(line)
        diagram, buttons, joltages = machine_configs

        # Find the shortest presss list from backtracking result
        curr = tuple('.' for i in range(len(diagram)))
        prev_buttons = ()
        total_num_presses += find_shortest_seq_presses(machine_configs, curr, prev_buttons)
        print(f'line #={i}')
    
    print(f'total number of presses = {total_num_presses}')

if __name__ == '__main__':
    main()

        

