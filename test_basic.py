#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import srctasks

class test__single_line_todo_finder(unittest.TestCase):

    def test_TODO_token(self):
        basic_test = '# TODO:content'
        answer = [srctasks.Todo(author='', task='content')]
        todos = srctasks._single_line_todo_finder(basic_test)
        self.assertEqual(todos, answer)

    def test_strip_leading_space_no_author(self):
        bad_whitespace = '# TODO:             \t content?'
        first_only, *_ = srctasks._single_line_todo_finder(bad_whitespace)
        self.assertEqual(first_only.task, 'content?')

    def test_strip_leading_space_with_author(self):
        bad_whitespace = '# TODO (  programmer ):             \t content?'
        first_only, *_ = srctasks._single_line_todo_finder(bad_whitespace)
        self.assertEqual(first_only.task, 'content?')
        self.assertEqual(first_only.author, 'programmer')

    def test_multiple_todos_no_author(self):
        many_todos = """# todo (me): task1
        // TODO: add another task
        /* todo: a third task
        */
        """
        first, second, third = srctasks._single_line_todo_finder(many_todos)
        self.assertEqual(first.task, 'task1')
        self.assertEqual(first.author, 'me')
        self.assertEqual(second.task, 'add another task')
        self.assertEqual(second.author, '')
        self.assertEqual(third.task, 'a third task')
        self.assertEqual(third.author, '')


    def test_many_tokens(self):
        pass

    def test_ignorecase(self):
        pass

    def test_case_sensitive(self):
        pass

if __name__ == '__main__':
    unittest.main()
