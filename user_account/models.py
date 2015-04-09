#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

#
# class BookManager(models.Manager):
#     def title_count(self, keyword):
#         return self.filter(title__icontains=keyword).count()
#
#
# class DahlBookManager(models.Manager):
#     def get_query_set(self):
#         return super(DahlBookManager, self).get_query_set().filter(author='Roald Dahl')


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __unicode__(self):
         return self.name


class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True)

    def __unicode__(self):
         return  u'%s %s' % (self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    # publication_date = models.DateField(blank=True, verbose_name='e-mail')
    # num_pages = models.IntegerField(blank=True, null=True)
    # objects = BookManager()
    # objects = models.Manager()           # The default manager.
    # dahl_objects = DahlBookManager()     # The Dahl-specific manager.

    def __unicode__(self):
         return self.title

#
# class MaleManager(models.Manager):
#     def get_query_set(self):
#         return super(MaleManager, self).get_query_set().filter(sex='M')
#
# class FemaleManager(models.Manager):
#     def get_query_set(self):
#         return super(FemaleManager, self).get_query_set().filter(sex='F')
