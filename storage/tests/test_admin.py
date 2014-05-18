# encoding: utf-8
'''
Copyright (c) 2013 Safari Books Online. All rights reserved.
'''

import uuid

from django.test import TestCase
import mock

from storage import models, admin

class TestBookAdmin(TestCase):
    def setUp(self):
        self.book = models.Book.objects.create(title="The Title", pk=str(uuid.uuid4()))
        self.alias1 = models.Alias.objects.create(book=self.book, scheme='ISBN-13', value='1000000000001')
        self.alias2 = models.Alias.objects.create(book=self.book, scheme='ISBN-10', value='1000000001')

        self.book_admin = admin.BookAdmin(models.Book, mock.Mock())

    def test_list_aliases(self):
        self.assertIn('list_aliases', self.book_admin.list_display)
        self.assertEqual(None, self.book_admin.list_aliases(None))

        expected = u'<pre>ISBN-10: 1000000001\nISBN-13: 1000000000001</pre>'
        self.assertEqual(expected, self.book_admin.list_aliases(self.book))
