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

def get_largest_num(battery_bank, num_rounds):
    """Get the largest number with num_rounds, say, 12,  digits from battery bank."""
    digits = [int(s) for s in battery_bank]
    total_digits = len(digits)
    left = 0
    result_num_list = []

    # Find the largest number for each of num_round rounds 
    for i in range(1, num_rounds + 1):    
        # Max heap used to find the next number in the sequence
        max_heap = []

        # Hash table for storing the first appearing index of a digit
        # within the index range from left to right.
        digit_idx_map = {}  # Key: number, value: index

        # The length of last chunk of digits not pushed onto max heap
        right_part_len = num_rounds - i  

        # The index of the rightmost number to be pushed on max heap
        right = total_digits - right_part_len - 1

        # Find the next number using heap
        if left <= right:
            for j in range(left, right + 1): 
                num = digits[j]
                heapq.heappush(max_heap, -num)
                if num not in digit_idx_map:
                    digit_idx_map[num] = j
            next_num = -heapq.heappop(max_heap)
            result_num_list.append(next_num)
            left = digit_idx_map[next_num] + 1
        else:
            if right_part_len != 0:
                result_num_list.extend(digits[right + 1:])
    
    return int(''.join([str(n) for n in result_num_list]))

def cal_output_joltage(battery_banks, num_rounds):
    """Calculate output joltage from all battery banks."""
    total_output_joltage = 0
    for battery_bank in battery_banks:
        total_output_joltage += get_largest_num(battery_bank, num_rounds)
    
    return total_output_joltage

battery_banks = get_lines('day3.txt')
num_rounds = 12
total_output_joltage = cal_output_joltage(battery_banks, num_rounds)
print(f'total output joltage = {total_output_joltage}')

