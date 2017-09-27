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


def _make_option(options):
    """Help make regex options from string

    Example:
        >>> _make_option('# // --')
        '(#|//|--)'
    """
    return '(' + '|'.join(options.split()) + ')'


def _single_line_todo_finder(text, comment_styles, tokens, seps, ignorecase):
    """Find and format tokens.

    Note:
        TODOs come in the form ``TOKEN (name): this is a task``
        A Todo has two attributes, author (name) and task (this is a task)

    Return:
        list of Todos.
    """
    # split line with token into username and task
    regex = (r'\s*' + comment_styles + r'\s*' + tokens
             + r'\s*((\()(?P<username>.*)(\)))?\s?' + seps + '(?P<task>.*)')
    search = re.compile(regex, 2 * ignorecase).search
    todos = []
    for line in text:
        match = search(line)
        if match:
            author = match.group('username').strip() \
                if match.group('username') else ''
            if match.group('task'):
                task = match.group('task').strip()
                todo = Todo(author, task)
                todos.append(todo)
    return todos


def _multiline_todo_finder(text, comment_styles, tokens, seps, bullets, ignorecase):
    """function not implemented. Todo finder for multiline lists.
    """
    # split line with token into username and task
    header = (
        r'\s*'
        + tokens
        + r'\s*((\()(?P<username>.*)(\)))?\s?'
        + seps
    )
    body = (
        r'\s*'
        + bullets
        + r'(?P<task>.*)'
    )
    find_head = re.compile(header, 2 * ignorecase).search
    find_body = re.compile(body, 2 * ignorecase).search
    todos = []
    is_bulleted_list = False
    task = None
    for line in text:
        if not is_bulleted_list:
            match = find_head(line)
            if match:
                is_bulleted_list = True
                author = match.group('username').strip() \
                    if match.group('username') else ''
        else:
            while task:
                task = find_body(line)
                if task:
                    todo = Todo(author, task)
                    todos.append(todo)
    return todos


def todo_finder(text,
                comment_styles='# // --',
                tokens='TODO',
                seps=':',
                ignorecase=True):
    """Find todos in single line and multiline comments."""
    text = text.splitlines()
    comment_styles = _make_option(comment_styles)
    tokens = _make_option(tokens)
    seps = _make_option(seps)
    bullets = r'\* \d\.? #\. -'
    bullets = _make_option(bullets)
    oneliners = _single_line_todo_finder(text, comment_styles, tokens, seps,
                                         ignorecase)
    multiliners = _multiline_todo_finder(text, comment_styles, tokens, seps,
                                         bullets, ignorecase)
    return oneliners + multiliners


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
        sub_dirs[:] = [sub_dir for sub_dir in sub_dirs
                       if sub_dir[0] not in hidden_prefix]
        for file in files:
            print(colorama.Fore.MAGENTA, colorama.Style.BRIGHT,
                  dir_name + os.sep + file, colorama.Style.RESET_ALL)
            with open(dir_name + os.sep + file) as source_code:
                try:
                    text = source_code.read()
                except UnicodeDecodeError:
                    text = ''  # not unicode inside
            todos = todo_finder(text)
            for todo in todos:
                print(fmt_todo(todo))


if __name__ == '__main__':
    main('/home/vincent/code')
