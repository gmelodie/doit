import argparse
from collections import OrderedDict
from typing import Dict

import os
import json
import re


class Task():
    def __init__(self, description: str, subtasks: list['Task'] = [], done=False, indent=0):
        self.description = description
        self.subtasks = subtasks
        self.done = done
        self.indent = indent

    def __repr__(self):
        return self.description

    def __eq__(self, other):
        if type(other) is str:
            return self.description == other
        return self.description == other.description


def get_cli_args():
    # Create the parser
    parser = argparse.ArgumentParser(description='TODO list CLI')

    # Add the arguments
    parser.add_argument('File',
                           metavar='file',
                           type=str,
                           help='the path to the TODO list')
    return parser.parse_args()


def get_tasks(md_filename):
    if not os.path.isfile(md_filename):
        print(f'Could not find the specified file {md_filename}')
        sys.exit()

    # parse markdown_text to raw todo list (unordered)
    with open(md_filename, 'r') as markdown_file:
        markdown_text = markdown_file.read()

    print(markdown_text)
    # for each line
    #   create new task node
    #   append to task list
    tasks = []
    line = re.compile(r'( *)- ([^\n]+)')
    for tabs, line in line.findall(markdown_text):
        indent = len(tabs)//4
        new_task = Task(description=line)
        tasks.append((indent, new_task))
    print(tasks)
    return tasks


def pop_task(unordered_tasks):
    # get first task with max indent (highest priority)
    max_indent, task = max(unordered_tasks, key=lambda x: x[0])
    unordered_tasks.remove((max_indent, task))
    return task


def doit(unordered_tasks):
    ordered_tasks = []

    # TODO: properly order tasks
    while len(unordered_tasks) != 0:
        next_task = pop_task(unordered_tasks)
        ordered_tasks.append(next_task)

    return ordered_tasks


if __name__ == '__main__':
    args = get_cli_args()
    md_filename = args.File

    unordered_tasks = get_tasks(md_filename)
    ordered_tasks = doit(unordered_tasks)
    print_tasks()

    # add the sugar to the list (most important first)
    # print(doit(raw_todo_list))
