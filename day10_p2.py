from functools import cache
import os
import re
from z3 import *


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

def generate_a_system_of_constraints(machine_configs):
    """Generate a system of constraints based on the config line."""
    #[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    diagram, buttons, joltages = machine_configs
    matrix = []
    for i in range(len(buttons)):
        button = buttons[i]  # button is a list of toggle locations
        line = []
        for j in range(len(diagram)):
            if j in button:
                num = 1
            else:
                num = 0
            line.append(num)
        
        matrix.append(line)

    # Generate variables
    vars_str = ['x' + str(i) for i in range(len(buttons))]
    vars_init_list = []
    for var_str in vars_str:
        var_init_str = f"{var_str} = Int('{var_str}')"
        vars_init_list.append(var_init_str)
    
    # Do column-wise addition
    constraints = []
    for col in range(len(diagram)):
        constraint_left = []
        for row, button in enumerate(buttons):
            if col in button:
                constraint_left.append(vars_str[row])
        
        constraint_left_str = ' + '.join(constraint_left)
        joltage_str = str(joltages[col])
        constraint_left_right = constraint_left_str + ' == ' + joltage_str
        constraints.append(constraint_left_right)

    # Add to constraints that every var is non-negative
    for var_str in vars_str:
        non_negative_constraint = f'{var_str} >= 0'
        constraints.append(non_negative_constraint)

    constraints_str = ', '.join(constraints)

    # Objective function
    objective_function_str = ' + '.join(vars_str)
    return constraints_str, vars_init_list, vars_str, objective_function_str

def solve_the_system(constraints_str, vars_init_list, vars_str, objective_function_str):
    vars = []
    opt = Optimize()

    for var_init in vars_init_list:
        exec(f'temp_expr = {var_init}', globals(), locals())

    for constraint_str in constraints_str.split(', '):
        # Use exec() to evaluate the string as Z3 Python code.
        # The result (a Z3 expression) is stored in the temporary variable 'temp_expr'.
        exec(f'temp_expr = {constraint_str}', globals(), locals())

        # The result of the exec is now available in the local variable 'temp_expr'
        z3_constraint = locals()['temp_expr']
        
        # Add the Z3 expression to the solver
        opt.add(z3_constraint)
        print(f"Added Z3 constraint: {z3_constraint}")

    # Prepare objective functions statement
    objective_function_statement = 'objective_function = ' + objective_function_str
    exec(f'temp_expr = {objective_function_statement}', globals(), locals())

    # Use the .minimize() method on the Optimize object
    opt_statement = 'opt.minimize(objective_function)'
    exec(f'temp_expr = {opt_statement}', globals(), locals())

    # 4. Solve the system
    print("\n--- Solving ---")
    statements = []
    statements.append('total_presses = 0')
    for var_str in vars_str:
        statement = f"print(f'{var_str} = {{m[{var_str}]}}')"
        statements.append(statement)
        statement = 'press_count = m[' + var_str + ']'
        statements.append(statement)
        statement = 'total_presses = total_presses + press_count.as_long()'
        statements.append(statement)
    statements.append(f"print(f'total_presses={{total_presses}}')")

    if opt.check() == sat:
        m = opt.model()
        print("Solution Found:")
        for statement in statements:
            exec(f'temp_expr = {statement}', globals(), locals())
        
        result = locals()['total_presses']
        print('----------------')
        print(f'result={result}')
        return result
    else:
        print("No solution found.")
        return 0


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

    # If the current joltages config is desirable, no need to press any button
    if curr == joltages:
        return 0
    
    # If any number in the joltage config is larger than the desired config, then stop
    for curr_joltage, joltage in zip(curr, joltages):
        if curr_joltage > joltage:
            return float('inf')
        
    options = []
    for button in buttons:
        new_config = list(curr)
        for toggle in button:
            new_config[toggle] += 1
            
        new_button_set = set(prev_buttons)
        new_button_set.add(button)
        press_number = find_shortest_seq_presses(machine_configs, tuple(new_config), frozenset(new_button_set)) + 1
        options.append(press_number)

    return min(options)

def main():
    lines = get_lines('day10.txt')
    total_num_presses = 0
    all_machine_configs = []
    for i, line in enumerate(lines):
        # Get each machine's configs
        machine_configs = get_machine_configs(line)

        system_constraints_str, vars_init_list, vars_str, objective_function_str = generate_a_system_of_constraints(machine_configs)
        print(system_constraints_str)
        total_num_presses += solve_the_system(system_constraints_str, vars_init_list, vars_str, objective_function_str)

        # Find the shortest presss list from backtracking result
        # curr = tuple(0 for i in range(len(diagram)))
        # prev_buttons = ()
        # total_num_presses += find_shortest_seq_presses(machine_configs, curr, prev_buttons)
        # print(f'line #={i}')
    
    print(f'total number of presses = {total_num_presses}')

if __name__ == '__main__':
    main()

        

