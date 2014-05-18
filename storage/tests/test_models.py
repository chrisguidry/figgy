# encoding: utf-8
'''
Copyright (c) 2013 Safari Books Online. All rights reserved.
'''

import uuid

from django.test import TestCase

from storage import models

class TestModels(TestCase):
    def setUp(self):
        self.book = models.Book.objects.create(title="The Title", pk=str(uuid.uuid4()))
        self.alias = models.Alias.objects.create(book=self.book, scheme='ISBN-13', value='1000000000001')

    def test_book_has_unicode_method(self):
        self.assertEquals('Book "The Title"', unicode(self.book))

    def test_alias_has_unicode_method(self):
        self.assertEquals('ISBN-13 identifier 1000000000001 for Book "The Title"', unicode(self.alias))