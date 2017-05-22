#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import srctasks

class test_todo_finder(unittest.TestCase):

    def test_TODO_token(self):
        basic_test = """This is not a comment
        # TODO:content

        also not a comment"""
        answer = [srctasks.Todo(author='', task='content')]
        todos = srctasks.todo_finder(basic_test)
        self.assertEqual(todos, answer)

    def test_TODO_author(self):
        basic_test = '#TODO(it\'sa Mario!):'
        answer = [srctasks.Todo(author='it\'sa Mario!', task='')]
        todos = srctasks.todo_finder(basic_test)
        self.assertEqual(todos, answer)

    def test_strip_leading_space_no_author(self):
        bad_whitespace = '# TODO:             \t content?'
        first_only, *_ = srctasks.todo_finder(bad_whitespace)
        self.assertEqual(first_only.task, 'content?')

    def test_strip_leading_space_with_author(self):
        bad_whitespace = '# TODO (  programmer ):             \t content?'
        first_only, *_ = srctasks.todo_finder(bad_whitespace)
        self.assertEqual(first_only.task, 'content?')
        self.assertEqual(first_only.author, 'programmer')

    def test_multiple_todos_no_author(self):
        many_todos = """lorem
        # todo (me): task1
        def a python function:
        ...

        // TODO: add another task

        todo_finder_function use case

        -- todo: a third task
        """
        first, second, third = srctasks.todo_finder(many_todos)
        self.assertEqual(first.task, 'task1')
        self.assertEqual(first.author, 'me')
        self.assertEqual(second.task, 'add another task')
        self.assertEqual(second.author, '')
        self.assertEqual(third.task, 'a third task')
        self.assertEqual(third.author, '')


    def test_many_tokens(self):
        many_tokens = """# todo ( person ): task
        # FIXME (fixer): fix
        -- CHANGED: a change
        // XXX: oops, a mistake
        # HACK: please don't do this one
        -- NOTE (good programmer) : I can leave notes.
        """
        todos = srctasks.todo_finder(many_tokens, tokens='todo fixme changed xxx hack note')
        first, second, third, fourth, fifth, sixth = todos
        self.assertEqual(first.task, 'task')
        self.assertEqual(first.author, 'person')
        self.assertEqual(second.task, 'fix')
        self.assertEqual(second.author, 'fixer')
        self.assertEqual(third.task, 'a change')
        self.assertEqual(third.author, '')
        self.assertEqual(fourth.task, 'oops, a mistake')
        self.assertEqual(fourth.author, '')
        self.assertEqual(fifth.task, 'please don\'t do this one')
        self.assertEqual(fifth.author, '')
        self.assertEqual(sixth.task, 'I can leave notes.')
        self.assertEqual(sixth.author, 'good programmer')


    def test_case_sensitive(self):
        tasks = """This is some code
        # Todo: don't pick me up
        -- TODO: I need to be done"""
        answer = [srctasks.Todo(author='', task='I need to be done')]
        todos = srctasks.todo_finder(tasks, ignorecase=False)
        self.assertEqual(todos, answer)

if __name__ == '__main__':
    unittest.main()
