
from rest_framework_filters import RelatedFilter
from rest_framework_filters.filterset import FilterSet

from relatedtest import models


class AuthorFilter(FilterSet):
    class Meta:
        model = models.Author
        fields = ['id', 'name']


class ChapterFilter(FilterSet):
    author = RelatedFilter(
        AuthorFilter,
        name='book__author',
        queryset=models.Author.objects.all(),
    )

    class Meta:
        model = models.Chapter
        fields = ['id', 'title', 'chapter_number', 'author']
