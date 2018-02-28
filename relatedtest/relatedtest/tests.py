"""Test filtering"""

from django.test import TestCase

from rest_framework.test import APIRequestFactory

from relatedtest.models import Book, Author, Chapter

from relatedtest import views


class ChapterTestCase(TestCase):

    def test_unfiltered_list(self):
        authors = [Author.objects.create(
            name=i
        ) for i in ['John Smith', 'Jane Doe', 'Nobody']]
        book = Book.objects.create(title='Something famous', author=authors[0])
        chapters = [Chapter.objects.create(
            book=book,
            chapter_number=i + 1,
            title=title,
            text=text,
        ) for i, (title, text) in enumerate([
            ('Title 1', 'Text 1'),
            ('Title 2', 'Text 2'),
        ])]
        factory = APIRequestFactory()
        view = views.ChapterViewSet.as_view({'get': 'list'})
        request = factory.get('/api/chapters/', format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(
            set(i['id'] for i in response.data['results']),
            set(i.id for i in chapters),
        )

    def test_filtered_list(self):
        """Attempt to use the related filter's name attribute"""
        # NOTE this test fails
        authors = [Author.objects.create(
            name=i
        ) for i in ['John Smith', 'Jane Doe', 'Nobody']]
        book = Book.objects.create(title='Something famous', author=authors[0])
        # dummy book by another author that will get excluded by the filter
        book_2 = Book.objects.create(
            title='Something famous', author=authors[1],
        )
        Chapter.objects.create(
            title='wheee', chapter_number=1, text="asdf", book=book_2,
        )
        chapters = [Chapter.objects.create(
            book=book,
            chapter_number=i + 1,
            title=title,
            text=text,
        ) for i, (title, text) in enumerate([
            ('Title 1', 'Text 1'),
            ('Title 2', 'Text 2'),
        ])]
        factory = APIRequestFactory()
        view = views.ChapterViewSet.as_view({'get': 'list'})
        request = factory.get(
            '/api/chapters/?author__name__icontains=john',
            format='json',
        )
        response = view(request)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(
            set(i['id'] for i in response.data['results']),
            set(i.id for i in chapters),
        )

    def test_id_lookup(self):
        """Just a sanity check of looking up by ID only"""
        authors = [Author.objects.create(
            name=i
        ) for i in ['John Smith', 'Jane Doe', 'Nobody']]
        # dummy book by another author that will get excluded by the filter
        book_2 = Book.objects.create(
            title='Something famous', author=authors[1],
        )
        Chapter.objects.create(
            title='wheee', chapter_number=1, text="asdf", book=book_2,
        )
        book = Book.objects.create(title='Something famous', author=authors[0])
        chapters = [Chapter.objects.create(
            book=book,
            chapter_number=i + 1,
            title=title,
            text=text,
        ) for i, (title, text) in enumerate([
            ('Title 1', 'Text 1'),
            ('Title 2', 'Text 2'),
        ])]
        factory = APIRequestFactory()
        view = views.ChapterViewSet.as_view({'get': 'list'})
        request = factory.get(
            '/api/chapters/?author=%s' % (authors[0].id, ),
            format='json',
        )
        response = view(request)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(
            set(i['id'] for i in response.data['results']),
            set(i.id for i in chapters),
        )
