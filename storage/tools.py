# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 4:58 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.

from storage.models import Book, Edition, Alias


def process_book_element(book_element):
    """
    Process a book element into the database.

    :param book: book element
    :returns:
    """

    version = book_element.findtext('version') or ''

    aliases = [(alias.get('scheme'), alias.get('value'))
               for alias in book_element.xpath('aliases/alias')]
    aliases.append(('Publisher ID', book_element.get('id')))

    title = book_element.findtext('title')
    description = book_element.findtext('description')

    # find any existing editions by any of these aliases
    existing_edition = Edition.most_likely_edition_by_aliases(aliases)
    if existing_edition:
        book = existing_edition.book
        if existing_edition.version == version:
            return
    else:
        book = Book.objects.create()

    new_edition = book.editions.create(title=title, description=description, version=version)
    for scheme, value in aliases:
        new_edition.aliases.get_or_create(scheme=scheme, value=value)
