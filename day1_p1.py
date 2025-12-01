import re
import collections
import math
import os
import pprint
import json
import sys

from functools import cache

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

