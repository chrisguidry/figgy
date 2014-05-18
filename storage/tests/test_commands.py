# encoding: utf-8
'''
Copyright (c) 2013 Safari Books Online. All rights reserved.
'''

import uuid

from django.test import TestCase
import mock

from storage.management.commands import process_data_file

class TestCommands(TestCase):
    def setUp(self):
        self.process_data_file = process_data_file.Command()

    def test_process_data_file(self):
        with mock.patch('storage.management.commands.process_data_file.open', create=True) as mock_open, \
             mock.patch('storage.management.commands.process_data_file.etree') as mock_etree, \
             mock.patch('storage.tools.process_book_element') as process_book_element:

            first_file, second_file = mock.Mock(), mock.Mock()
            mock_open.return_value.__enter__.side_effect = [first_file, second_file]

            first_etree, second_etree = mock.Mock(), mock.Mock()
            mock_etree.parse.side_effect = [first_etree, second_etree]

            self.process_data_file.handle('file1', 'file2')

            mock_open.assert_has_calls([
                mock.call('file1', 'rb'),
                mock.call('file1', 'rb').__enter__(),
                mock.call('file1', 'rb').__exit__(None, None, None),

                mock.call('file2', 'rb'),
                mock.call('file2', 'rb').__enter__(),
                mock.call('file2', 'rb').__exit__(None, None, None)
            ])

            mock_etree.parse.assert_has_calls([
                mock.call(first_file),
                mock.call(second_file)
            ])

            process_book_element.assert_has_calls([
                mock.call(first_etree.getroot.return_value),
                mock.call(second_etree.getroot.return_value)
            ])
