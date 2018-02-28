
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


from . import models
from . import filters
from . import serializers


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.AuthorFilter
    serializer_class = serializers.AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.select_related('author')
    filter_backends = (DjangoFilterBackend, )
    serializer_class = serializers.BookSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = models.Chapter.objects.select_related('book__author')
    filter_backends = (DjangoFilterBackend, )
    serializer_class = serializers.ChapterSerializer
    filter_class = filters.ChapterFilter
