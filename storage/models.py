# encoding: utf-8

from django.db import models
from django.db.models import Q


class BaseModel(models.Model):
    '''Base class for all models'''
    created_time = models.DateTimeField('date created', auto_now_add=True)
    last_modified_time = models.DateTimeField('last-modified', auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Book(BaseModel):
    '''
    Main storage for a Book object.
    '''

    id = models.AutoField(primary_key=True, help_text='Our unique identifier for this book.')

    class Meta:
        ordering = ['created_time']


class Edition(BaseModel):
    book = models.ForeignKey(Book, related_name='editions')
    version = models.CharField(max_length=20, blank=True, help_text="A publisher-provided version for this edition.")
    title = models.CharField(max_length=128, help_text="The title of this book.", db_index=True, null=False, blank=False)
    description = models.TextField(blank=True, null=True, default=None, help_text="Very short description of this book.")

    @classmethod
    def most_likely_edition_by_aliases(cls, aliases):
        '''
        Given a list of (scheme,value) pairs, find the most likely
        Edition uniquely referenced by those aliases.
        '''

        # find editions which have any of the given aliases
        alias_filter = Q()
        for scheme, value in aliases:
            alias_filter |= Q(scheme=scheme, value=value)
        alias_query = Alias.objects.filter(alias_filter)
        possible_editions = list(cls.objects.filter(aliases__in=alias_query))

        if not possible_editions:
            return None

        # order the editions by the count of matching aliases
        provided_aliases = set(aliases)
        def count_of_matching_aliases(edition):
            edition_aliases = {(alias.scheme, alias.value) for alias in edition.aliases.all()}
            return len(edition_aliases & provided_aliases)
        possible_editions.sort(key=count_of_matching_aliases)

        # return the highest one
        return possible_editions[-1]

    class Meta:
        ordering = ['version']


class Alias(BaseModel):
    '''
    A book can have one or more aliases which

    For example, a book can be referred to with an ISBN-10 (older, deprecated scheme), ISBN-13 (newer scheme),
    or any number of other aliases.
    '''

    edition = models.ForeignKey(Edition, related_name='aliases')
    scheme = models.CharField(max_length=40, help_text="The scheme of identifier")
    value = models.CharField(max_length=255, db_index=True, help_text="The value of this identifier")
