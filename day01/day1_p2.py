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

def get_steps(lines):
    """Get the steps for unlocking the safe.
    
    Args:
        lines (list): Input lines from the text file.

    Returns:
        A list of steps each of which is a tuple, e.g., ('L', 30).
    """
    steps = []
    for line in lines:
        direction = line[0]
        counts = int(line[1:])
        steps.append((direction, counts))
    
    return steps

def get_num_zeros(steps, start_num):
    """Calculate the number of times reaching zero.
    
    Args:
        steps (list): A list of steps each of which is a tuple like ('L', 580)
        start_num: The start number on the dial

    Returns:
        The number of time the arrow on the lock pointing to zero.
    """

    zero_count = 0
    curr_num = start_num
    for direction, step in steps:
        print(f'before -- number is {curr_num}, turn is {direction}, {step}')
        if step >= 100:
            zero_count += step // 100
            step = step % 100
    
        if direction == 'L':
            if curr_num != 0 and curr_num <= step:
                zero_count += 1
            curr_num = (curr_num - step) % 100     
        else:
            if curr_num + step >= 100:
                zero_count += 1
            curr_num = (curr_num + step) % 100
        
        print(f'after -- number is {curr_num}, zero_count={zero_count}')
        print('==================')

    return zero_count

lines = get_lines('day1.txt')
steps = get_steps(lines)
num_zeros = get_num_zeros(steps, 50)
print(num_zeros)