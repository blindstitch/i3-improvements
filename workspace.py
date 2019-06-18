#!/usr/bin/env python3
# workspace.py
# Move, switch, and rename workspaces without numbering them
#
#  - Untested for first boot

from i3 import *
import argparse
import subprocess
from random import randint

from pprint import PrettyPrinter
pp = PrettyPrinter(); pprint = lambda x: pp.pprint(x)

# Args
parser = argparse.ArgumentParser(description='i3wm workspace controls')
parser.add_argument('--goto',help='Goto workspace N',nargs='?')
parser.add_argument('--move',choices=['left','right'],help='Move workspace',nargs='?')
parser.add_argument('--move_test',choices=['left','right'],help='Move workspace',nargs='?')
parser.add_argument('--command',choices=['new','rename'],help='Command',nargs='?')
parser.add_argument('--move_container',choices=['left','right'],help='Command',nargs='?')
args = parser.parse_args()

# Vars
spaces = get_spaces()
space_names = [space['name'] for space in spaces]
space_name = get_active_space_name()
space_index = [i for i,s in enumerate(spaces) if s['name'] == space_name][0]
spaces_after = space_names[space_index+1:]
spaces_after = space_names[space_index+1:]
spaces_before = space_names[:space_index]
space_left = space_names[space_index-1]

# Basic command pieces
commands = {
    'goto' : ['i3-msg', 'workspace'],
    'rename-input': ['i3-input', "-P", "'Rename", "workspace:", "'"],
    'rename' : ["i3-msg", "rename", "workspace", "to"]
}

# Goto space
def goto(num):
    if num == 0:
        subprocess.call(commands['goto'] + [spaces[-1]['name']])
    if num == 9:
        subprocess.call(commands['goto'] + [spaces[-2]['name']])
    else:
        name = spaces[num - 1]['name']
        subprocess.call(commands['goto'] + [name])

# Rename space/s to current name
def rename_in_place(space_or_spaces):
    if isinstance(space_or_spaces,list):
        for space in space_or_spaces:
            subprocess.call(['i3-msg','rename','workspace',space,'to',space])
    if isinstance(space_or_spaces,str):
        subprocess.call(['i3-msg','rename','workspace',space_or_spaces,'to',space_or_spaces])

# Move space
def move(direction):
    if (direction == 'left') & (space_index != 0):
        rename_in_place(space_name)  # Put at end
        rename_in_place(space_left)
        for space in spaces_after:
            rename_in_place(space)
    if (direction == 'right') & (space_index != len(spaces)-1):
        rename_in_place(space_name) # Put at end
        for space in space_names[space_index+2:]:
            rename_in_place(space)

# Rename space
def rename_space(name):
    subprocess.call(commands['rename'] + [name])
    rename_in_place(spaces_after)

# Rename prompt
def rename_prompt():
    p = subprocess.Popen('i3-input', stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p.wait()
    output = output.decode('UTF-8')
    command = output.split('\n')[-2]
    if command.startswith('command = '):
        clean_name = command.replace('command = ','').replace(' ','-')
        rename_space(clean_name)
    else:
        print('No i3 input parsed, did you press escape, or enter nothing?')
        exit()

# New workspace, uses a random vegetable for the name.
def new():
    new_name = vegetables[randint(0,len(vegetables)-1)]
    subprocess.call(commands['goto'] + [new_name])

def move_container_to_workspace(direction):
    if (direction == 'left') & (space_index != 0):
        subprocess.call(['i3-msg', 'move','container','to','workspace',space_left])
        subprocess.call(['i3-msg', 'workspace','prev'])
    if (direction == 'right') & (space_index != len(spaces)-1):
        subprocess.call(['i3-msg', 'move','container','to','workspace',space_names[space_index+1]])
        subprocess.call(['i3-msg', 'workspace','next'])

# Parse arguments
print(args.command)
if args.goto is not None:
    goto(int(args.goto))
elif args.move is not None:
    move(args.move)
elif args.move_container is not None:
    move_container_to_workspace(args.move_container)
elif args.command == 'rename':
    rename_prompt()
elif args.command == 'new':
    new()
else:
    parser.print_help()
