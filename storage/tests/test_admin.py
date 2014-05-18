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
        self.book = models.Book.objects.create()

        first_edition = models.Edition.objects.create(book=self.book, title="The Title, First Edition",
                                                      description='A great read!')
        models.Alias.objects.create(edition=first_edition, scheme='ISBN-13', value='1000000000001')
        models.Alias.objects.create(edition=first_edition, scheme='ISBN-10', value='1000000001')

        second_edition = models.Edition.objects.create(book=self.book, title="The Title, Second Edition",
                                                       description='A tour de force!')
        models.Alias.objects.create(edition=second_edition, scheme='ISBN-13', value='1000000000002')
        models.Alias.objects.create(edition=second_edition, scheme='ISBN-10', value='1000000002')

        self.book_admin = admin.BookAdmin(models.Book, mock.Mock())

    def test_list_aliases(self):
        self.assertIn('list_aliases', self.book_admin.list_display)
        self.assertEqual(None, self.book_admin.list_aliases(None))

        expected = (u'<pre>ISBN-10: 1000000001\nISBN-13: 1000000000001</pre>'+
                    u'<pre>ISBN-10: 1000000002\nISBN-13: 1000000000002</pre>')
        self.assertEqual(expected, self.book_admin.list_aliases(self.book))

    def test_list_editions(self):
        self.assertIn('list_editions', self.book_admin.list_display)
        self.assertEqual(None, self.book_admin.list_editions(None))

        expected = (u'<h3>The Title, First Edition</h3><p>A great read!</p>'+
                    u'<h3>The Title, Second Edition</h3><p>A tour de force!</p>')
        self.assertEqual(expected, self.book_admin.list_editions(self.book))
