"""Stupidly simple proof-of-concept models"""


from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, models.DO_NOTHING, related_name='books')

    class Meta:
        unique_together = (('title', 'author'), )


class Chapter(models.Model):
    title = models.CharField(max_length=50)
    chapter_number = models.PositiveSmallIntegerField()
    book = models.ForeignKey(Book, models.DO_NOTHING, related_name='chapters')
    text = models.TextField()

    class Meta:
        unique_together = (('book', 'chapter_number'), )
