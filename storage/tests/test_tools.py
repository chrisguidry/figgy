# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 5:01 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.

from django.test import TestCase
from lxml import etree

from storage.models import Book, Edition, Alias
import storage.tools


class TestTools(TestCase):
    def setUp(self):
        pass

    def test_process_book_element_new_book(self):
        '''process_book_element should put the book in the database.'''

        storage.tools.process_book_element(etree.fromstring('''
        <book id="12345">
            <title>A title</title>
            <version>1.0</version>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''))

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.all()[0]

        self.assertEqual(book.editions.count(), 1)
        edition = book.editions.all()[0]

        self.assertEqual(edition.aliases.count(), 3)
        self.assertEqual(edition.aliases.get(scheme='Publisher ID').value, '12345')
        self.assertEqual(edition.aliases.get(scheme='ISBN-10').value, '0158757819')
        self.assertEqual(edition.aliases.get(scheme='ISBN-13').value, '0000000000123')

    def test_process_book_element_existing_book(self):
        '''process_book_element should put the book in the database.'''

        existing_book = Book.objects.create()
        existing_edition = existing_book.editions.create(title='Old Title', version='0.1')
        existing_edition.aliases.create(scheme='Publisher ID', value='12345')
        existing_edition.aliases.create(scheme='ISBN-13', value='0000000000123')
        existing_edition.aliases.create(scheme='ISBN-10', value='different')

        storage.tools.process_book_element(etree.fromstring('''
        <book id="12345">
            <title>A title</title>
            <version>1.0</version>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''))

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.all()[0]

        self.assertEqual(book.editions.count(), 2)
        new_edition = book.editions.exclude(pk=existing_edition.pk)[0]

        self.assertEqual(new_edition.aliases.count(), 3)
        self.assertEqual(new_edition.aliases.get(scheme='Publisher ID').value, '12345')
        self.assertEqual(new_edition.aliases.get(scheme='ISBN-10').value, '0158757819')
        self.assertEqual(new_edition.aliases.get(scheme='ISBN-13').value, '0000000000123')
