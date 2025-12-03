import os
import heapq

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

def get_largest_num(battery_bank):
    """Get the largest number with two digits from battery bank."""
    digits = [int(s) for s in battery_bank]
    first_appearing_index = {}

    for i, num in enumerate(digits):
        if num not in first_appearing_index:
            first_appearing_index[num] = i

    # Push all digits into a max heap
    max_heap = []
    for i in range(0, len(digits) - 1):
        heapq.heappush(max_heap, -digits[i])

    # Get the first number from the heap
    first_num = -heapq.heappop(max_heap)
    max_heap = []

    # Get the second number from the heap
    start = first_appearing_index[first_num] + 1
    for i in range(start, len(digits)):
        heapq.heappush(max_heap, -digits[i])
    second_num = -heapq.heappop(max_heap)

    # Form the result from both numbers
    result = int(str(first_num) + str(second_num))
    return result

def cal_output_joltage(battery_banks):
    """Calculate output joltage from all battery banks."""
    total_output_joltage = 0
    for battery_bank in battery_banks:
        total_output_joltage += get_largest_num(battery_bank)
    
    return total_output_joltage

battery_banks = get_lines('day3.txt')
total_output_joltage = cal_output_joltage(battery_banks)
print(f'total output joltage = {total_output_joltage}')

