#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO:
    * Mock the todo_finder not in use
"""

import unittest

import srctasks


class test_todo_finder_single_line_comments(unittest.TestCase):

    def test_TODO_token(self):
        basic_test = """This is not a comment
        # TODO:content

        also not a comment"""
        answer = [srctasks.Todo(author='', task='content')]
        todos = srctasks.todo_finder(basic_test)
        self.assertEqual(todos, answer)

    def test_TODO_author(self):
        basic_test = '#TODO(it\'sa Mario!): some noise'
        answer = [srctasks.Todo(author='it\'sa Mario!', task='some noise')]
        todos = srctasks.todo_finder(basic_test)
        self.assertEqual(todos, answer)

    def test_strip_leading_space_no_author(self):
        bad_whitespace = '# TODO:             \t content?'
        answer = [srctasks.Todo(author='', task='content?')]
        todos = srctasks.todo_finder(bad_whitespace)
        self.assertEqual(todos, answer)

    def test_strip_leading_space_with_author(self):
        bad_whitespace = '# TODO (  programmer ):             \t content?'
        answer = [srctasks.Todo(author='programmer', task='content?')]
        todos = srctasks.todo_finder(bad_whitespace)
        self.assertEqual(todos, answer)

    def test_multiple_todos_no_author(self):
        many_todos = """lorem
        # todo (me): task1
        def a python function:
        ...

        // TODO: add another task

        todo_finder_function use case

        -- todo: a third task
        """
        answer = [
            srctasks.Todo(author='me', task='task1'),
            srctasks.Todo(author='', task='add another task'),
            srctasks.Todo(author='', task='a third task')
        ]
        todos = srctasks.todo_finder(many_todos)
        self.assertEqual(todos, answer)

    def test_many_tokens(self):
        many_tokens = """# todo ( person ): task
        # FIXME (fixer): fix
        -- CHANGED: a change
        // XXX: oops, a mistake
        # HACK: please don't do this one
        -- NOTE (good programmer) : I can leave notes.
        """
        answer = [
            srctasks.Todo(author='person', task='task'),
            srctasks.Todo(author='fixer', task='fix'),
            srctasks.Todo(author='', task='a change'),
            srctasks.Todo(author='', task='oops, a mistake'),
            srctasks.Todo(author='', task='please don\'t do this one'),
            srctasks.Todo(author='good programmer', task='I can leave notes.')
        ]
        todos = srctasks.todo_finder(many_tokens, tokens='todo fixme changed xxx hack note')
        self.assertEqual(todos, answer)

    def test_case_sensitive(self):
        tasks = """This is some code
        # Todo: don't pick me up
        -- TODO: I need to be done"""
        answer = [srctasks.Todo(author='', task='I need to be done')]
        todos = srctasks.todo_finder(tasks, ignorecase=False)
        self.assertEqual(todos, answer)


# class test_todo_finder_multiline_comments(unittest.TestCase):

#     def test_across_multiple_lines(self):
#         test = '''
#             TODO:
#                 * implement this
#                 * test it
#                 * document it
#         '''

#         answer = [
#             srctasks.Todo(author='', task='implement this'),
#             srctasks.Todo(author='', task='test it'),
#             srctasks.Todo(author='', task='document it'),
#         ]
#         todos = srctasks.todo_finder(test)
#         self.assertEqual(todos, answer)

#     def test_on_same_line(self):
#         test = '''

#         def foo(x):
#             """A docstring

#             TODO:
#                 * implement this
#                 * test it
#                 * document it

#             """

#         '''

#         answer = [
#             srctasks.Todo(author='', task='implement this'),
#             srctasks.Todo(author='', task='test it'),
#             srctasks.Todo(author='', task='document it'),
#         ]
#         todos = srctasks.todo_finder(test)
#         self.assertEqual(todos, answer)

#     def test_on_bad_whitespace(self):
#         test = '''

#         def foo(x):

#             TODO:
#                 * implement this
#                 * test it
#                 * document it
#         '''
#         answer = [
#             srctasks.Todo(author='', task='implement this'),
#             srctasks.Todo(author='', task='test it'),
#             srctasks.Todo(author='', task='document it'),
#         ]
#         todos = srctasks.todo_finder(test)
#         self.assertEqual(todos, answer)

#     def test_author(self):
#         test = '''

#         def foo(x):
#             """A docstring

#             TODO:
#                 * implement this
#                 * test it
#                 * document it

#             """

#         '''

#         answer = [
#             srctasks.Todo(author='', task='implement this'),
#             srctasks.Todo(author='', task='test it'),
#             srctasks.Todo(author='', task='document it'),
#         ]
#         todos = srctasks.todo_finder(test)
#         self.assertEqual(todos, answer)

#     def test_with_many_tokens(self):
#         test = '''

#         def foo(x):
#             """A docstring

#             TODO:
#                 * implement this
#                 * test it
#                 * document it

#             """

#         '''

#         answer = [
#             srctasks.Todo(author='', task='implement this'),
#             srctasks.Todo(author='', task='test it'),
#             srctasks.Todo(author='', task='document it'),
#         ]
#         todos = srctasks.todo_finder(test)
#         self.assertEqual(todos, answer)

#     def test_many_bullet_types(self):
#         test = '''

#         def foo(x):
#             """A docstring

#             TODO:
#                 * implement this
#                 * test it
#                 * document it

#             """

#         '''

#         answer = [
#             srctasks.Todo(author='', task='implement this'),
#             srctasks.Todo(author='', task='test it'),
#             srctasks.Todo(author='', task='document it'),
#         ]
#         todos = srctasks.todo_finder(test)
#         self.assertEqual(todos, answer)


if __name__ == '__main__':
    unittest.main()
