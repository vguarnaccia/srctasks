#! /usr/bin/env python3
"""Find TODOs in source code.

TODO:
    * Better format TODOs
    * Add docstring style TODOs like these.
"""

import collections
import os
import re

import colorama

colorama.init()
Todo = collections.namedtuple('Todo', ['author', 'task'])


def todo_finder(filepath):
    """Find and format TODOs in a sting

    Note:
        TODOs come in the form ``TODO (name): this is a comment``

    Return:
        Indented TODO list block
    """
    with open(filepath) as source_code:
        try:
            # TODO (Vincent): write using readlines so it can be enumerated
            text = source_code.read()
        except UnicodeDecodeError:
            text = '' # not unicode inside

        # Inline TODOs
        matches = re.finditer(r'TODOS?\s*(?P<username>\(\w*\s*\w*\))?:*\s?(?P<task>.*)',
                              text, re.IGNORECASE | re.MULTILINE)
        todos = []
        for match in matches:
            author = '<%s>' % match.group('username') if match.group('username') else ''
            task = match.group('task')
            todo = Todo(author, task)
            todos.append(todo)
        return todos



def main(root):
    """Apply todo_finder on each file in directory.
    """
    hidden_prefix = ('.', '_')
    for dir_name, sub_dirs, files in os.walk(root):
        # Remove hidden folders and add a suffix
        sub_dirs[:] = [sub_dir for sub_dir in sub_dirs if sub_dir[0] not in hidden_prefix]
        for file in files:
            print(
                colorama.Fore.MAGENTA,
                colorama.Style.BRIGHT,
                dir_name + os.sep + file,
                colorama.Style.RESET_ALL
            )
            todos = todo_finder(os.path.join(dir_name, file))
            for todo in todos:
                print(todo.task.strip(), todo.author)


if __name__ == '__main__':
    main('/home/vincent/code')
