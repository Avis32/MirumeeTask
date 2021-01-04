from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase, Client

from book_search.models import Book, Author, Type, Review


class TestBookListView(TestCase):
    def setUp(self) -> None:
        self.author = Author.objects.create(full_name='a')
        self.book_type = Type.objects.create(type_name='a')
        Book.objects.bulk_create(
            [
                Book(isbn=1, title='aa', author=self.author, type=self.book_type),
                Book(isbn=2, title='bb', author=self.author, type=self.book_type),
                Book(isbn=3, title='cc', author=self.author, type=self.book_type),
                Book(isbn=4, title='cd', author=self.author, type=self.book_type),
                Book(isbn=5, title='ee', author=self.author, type=self.book_type),
             ]
        )

    def test_if_book_is_found_with_query(self):
        response = self.client.get('/books/search/', {'q': 'a', 'page': 0})
        self.assertJSONEqual(
            response.content, {'books': [{'isbn': 1, 'title': 'aa', 'author': 1, 'type': 'a'}]}
        )

    def test_if_books_search_returns_only_query_matching_books(self):
        response = self.client.get('/books/search/', {'q': 'c', 'page': 0})
        books_checked = []
        for book in response.json()['books']:
            self.assertNotIn(book['isbn'], books_checked, 'same book returned twice')
            books_checked.append(book['isbn'])
        self.assertEqual(len(books_checked), 2)

    def tests_if_books_search_endpoint_return_only_10_results(self):
        Book.objects.all().delete()
        for x in range(20):
            Book.objects.create(isbn=x, title='zz', author=self.author, type=self.book_type)
        response = self.client.get('/books/search/', {'page': 0})
        self.assertEqual(len(response.json()['books']), 10)

    def test_if_books_are_ordered_by_isbn(self):
        Book.objects.all().delete()
        number_of_books_to_create = 10
        for x in range(number_of_books_to_create):
            Book.objects.create(isbn=number_of_books_to_create-x, title='zz', author=self.author, type=self.book_type)
        response = self.client.get('/books/search/', {'page': 0})
        last_isbn = None
        for book in response.json()['books']:
            isbn = book['isbn']
            if not last_isbn:
                last_isbn = isbn
                continue
            self.assertTrue(isbn > last_isbn, 'Books have wrong order')

    def test_if_book_list_view_query_param_is_case_insensitive(self):
        isbn_number = Book.objects.all().order_by('-isbn').first().isbn + 1
        Book.objects.create(isbn=isbn_number, title='tEsT_bOoK', author=self.author, type=self.book_type)
        response = self.client.get('/books/search/', {'q': 'test'})
        self.assertEqual(response.json()['books'][0]['isbn'], isbn_number)


class TestBookDetailView(TestCase):
    def setUp(self) -> None:
        self.author = Author.objects.create(full_name='a')
        self.book_type = Type.objects.create(type_name='a')
        self.book_1 = Book.objects.create(isbn=1, title='aa', author=self.author, type=self.book_type)
        self.reviews_for_book_1 = [Review.objects.create(book=self.book_1, score=1, review=str(x)) for x in range(10)]
        self.book_2 = Book.objects.create(isbn=2, title='aa', author=self.author, type=self.book_type)
        self.reviews_for_book_2 = [Review.objects.create(book=self.book_2, score=1, review=str(x)) for x in range(10)]

    def test_if_book_reviews_are_returned(self):
        response = self.client.get('/books/{}/'.format(self.book_1.isbn))
        self.assertNotEqual(response.json()['reviews'], [])

    def test_if_reviews_are_from_correct_book(self):
        response = self.client.get('/books/{}/'.format(self.book_1.isbn))
        for review in response.json()['reviews']:
            self.assertEqual(review['book'], self.book_1.isbn)


