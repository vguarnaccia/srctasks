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


def _single_line_todo_finder(text, comment_styles='# // --', tokens='TODO',
                             seps=':', ignorecase=True):
    """Find and format tokens.

    Note:
        TODOs come in the form ``TOKEN (name): this is a task``
        A Todo has two attributes, author (name) and task (this is a task)

    Return:
        list of Todos.
    """
    make_option = lambda s: '(' + '|'.join(s.split()) + ')'
    text = text.splitlines()
    comment_styles = make_option(comment_styles)
    tokens = make_option(tokens)
    seps = make_option(seps)
    # split line with token into username and task
    regex = (
        r'\s*'
        + comment_styles
        + r'\s*'
        + tokens
        + r'\s*((\()(?P<username>.*)(\)))?\s?'
        + seps
        +  '(?P<task>.*)'
    )
    search = re.compile(regex, re.IGNORECASE if ignorecase else 0).search
    todos = []
    for line in text:
        match = search(line)
        if match:
            author = match.group('username').strip() if match.group('username') else ''
            task = match.group('task').strip()
            todo = Todo(author, task)
            todos.append(todo)
    return todos


def _multiline_todo_finder(text, comment_styles='# // --', tokens='TODO',
                           seps=':', ignorecase=True):
    """function not implemented. Todo finder for multiline lists.
    """
    todos = []
    return todos

def todo_finder(text, comment_styles='# // --', tokens='TODO', seps=':', ignorecase=True):
    """Find todos in single line and multiline comments."""
    return (_single_line_todo_finder(text, comment_styles, tokens, seps, ignorecase)
            + _multiline_todo_finder(text, comment_styles, tokens, seps, ignorecase))

def fmt_todo(todo):
    """Colorize and format a list of todos
    """
    author = ' <%s>' % todo.author
    task = todo.task
    return task + author


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
            with open(dir_name + os.sep + file) as source_code:
                try:
                    text = source_code.read()
                except UnicodeDecodeError:
                    text = '' # not unicode inside
            todos = todo_finder(text)
            for todo in todos:
                print(fmt_todo(todo))


if __name__ == '__main__':
    main('/home/vincent/code')
