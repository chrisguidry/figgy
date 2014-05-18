# encoding: utf-8
'''
Copyright (c) 2013 Safari Books Online. All rights reserved.
'''

import uuid

from django.test import TestCase

from storage.models import Book, Edition, Alias

class TestModels(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create()

        self.book1_first = self.book1.editions.create(title="The Title, First Edition",
                                                      description='A great read!')
        self.book1_first.aliases.create(scheme='ISBN-13', value='1000000000001')
        self.book1_first.aliases.create(scheme='ISBN-10', value='1000000001')

        self.book1_second = self.book1.editions.create(title="The Title, Second Edition",
                                                       description='A tour de force!')
        self.book1_second.aliases.create(scheme='ISBN-13', value='1000000000002')
        self.book1_second.aliases.create(scheme='ISBN-10', value='1000000002')

        self.book2 = Book.objects.create()

        self.book2_first = self.book2.editions.create(title="A Different One",
                                                      description='A terrible read!')
        self.book2_first.aliases.create(scheme='ISBN-13', value='1000000000002')
        self.book2_first.aliases.create(scheme='ISBN-10', value='1000000001')

    def test_most_likely_edition_exact_match(self):
        edition = Edition.most_likely_edition_by_aliases([('ISBN-13', '1000000000001'),
                                                          ('ISBN-10', '1000000001')])
        self.assertEqual(self.book1_first.pk, edition.pk)

    def test_most_likely_edition_partial_match(self):
        edition = Edition.most_likely_edition_by_aliases([('ISBN-13', '1000000000001')])
        self.assertEqual(self.book1_first.pk, edition.pk)

    def test_most_likely_edition_favors_more_aliases(self):
        edition = Edition.most_likely_edition_by_aliases([('ISBN-13', '1000000000002'),
                                                          ('ISBN-10', '1000000001')])
        self.assertEqual(self.book2_first.pk, edition.pk)

    def test_most_likely_edition_favors_no_matches(self):
        edition = Edition.most_likely_edition_by_aliases([('ISBN-13', 'nope'),
                                                          ('ISBN-10', 'never')])
        self.assertIsNone(edition)
