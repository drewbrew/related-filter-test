"""proof-of-concept serializers"""

from rest_framework import serializers

from relatedtest import models


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = models.Author


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return AuthorSerializer(obj.book.author)

    class Meta:
        model = models.Chapter
        fields = '__all__'
