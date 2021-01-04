import os
from io import StringIO
from pathlib import Path, PosixPath
from unittest.mock import patch, mock_open

from django.core.management import call_command
from django.test import TestCase

from book_search.models import Book, Type, Author, Review


class TestLoadCommandsFromCSVFileCommand(TestCase):
    BOOKS_FILE_NAME = 'ksiazki.csv'
    REVIEWS_FILE_NAME = 'Opinie.csv'
    TEST_FILE_LINE_COUNT = 10

    def setUp(self) -> None:
        self.relative_path = self._build_relative_path_to_test_data_folder()
        self._create_temp_book_csv_file(self.relative_path)

    def tearDown(self) -> None:
        self._remove_temp_book_csv_file(self.relative_path)

    def _build_relative_path_to_test_data_folder(self) -> str:
        base_path = Path(__file__).parent
        return str((base_path / "./test_data/").resolve())

    def _create_temp_book_csv_file(self, path):
        with open(path + '/' + self.BOOKS_FILE_NAME, 'w') as f:
            f.write('ISBN;Tytuł;Autor;Gatunek;\n')
            for x in range(self.TEST_FILE_LINE_COUNT):
                f.write('{isbn};{title};{author};{type};\n'.format(isbn=x, title=x, author=x, type=x))

    def _remove_temp_book_csv_file(self, path):
        os.remove(path + '/' + self.BOOKS_FILE_NAME)

    def test_if_books_are_created_successfully(self):
        call_command('load_books_from_csv', self.relative_path + '/' + self.BOOKS_FILE_NAME)
        self.assertEqual(Book.objects.count(), self.TEST_FILE_LINE_COUNT)

    def test_if_command_dont_create_multiple_instances(self):
        call_command('load_books_from_csv', self.relative_path + '/' + self.BOOKS_FILE_NAME)
        author_count = Author.objects.count()
        book_type_count = Type.objects.count()
        book_count = Book.objects.count()
        call_command('load_books_from_csv', self.relative_path + '/' + self.BOOKS_FILE_NAME)
        self.assertEqual(Book.objects.count(), book_count)
        self.assertEqual(Author.objects.count(), author_count)
        self.assertEqual(Type.objects.count(), book_type_count)


class TestCreateReviewsFromCSVFile(TestCase):
    BOOKS_FILE_NAME = 'ksiazki.csv'
    REVIEWS_FILE_NAME = 'Opinie.csv'
    TEST_FILE_LINE_COUNT = 10

    def setUp(self) -> None:
        self.relative_path = self._build_relative_path_to_test_data_folder()
        self._create_temp_book_csv_file(self.relative_path)
        self._create_temp_review_csv_file(self.relative_path)
        call_command('load_books_from_csv', self.relative_path + '/' + self.BOOKS_FILE_NAME)

    def tearDown(self) -> None:
        self._remove_temp_book_csv_file(self.relative_path)
        self._remove_temp_review_csv_file(self.relative_path)

    @staticmethod
    def _build_relative_path_to_test_data_folder() -> str:
        base_path = Path(__file__).parent
        return str((base_path / "./test_data/").resolve())

    def _create_temp_book_csv_file(self, path):
        with open(path + '/' + self.BOOKS_FILE_NAME, 'w') as f:
            f.write('ISBN;Tytuł;Autor;Gatunek;\n')
            for x in range(self.TEST_FILE_LINE_COUNT):
                f.write('{isbn};{title};{author};{type};\n'.format(isbn=x, title=x, author=x, type=x))

    def _create_temp_review_csv_file(self, path):
        with open(path + '/' + self.REVIEWS_FILE_NAME, 'w') as f:
            f.write('ISNB;Ocena;Opis;\n')
            for x in range(self.TEST_FILE_LINE_COUNT):
                f.write('{isbn};{score};{review};\n'.format(isbn=x, score=x, review=x))

    def _remove_temp_review_csv_file(self, path):
        os.remove(path + '/' + self.REVIEWS_FILE_NAME)

    def _remove_temp_book_csv_file(self, path):
        os.remove(path + '/' + self.BOOKS_FILE_NAME)

    def test_if_reviews_are_created_successfully(self):
        call_command('load_reviews_from_csv', self.relative_path + '/' + self.REVIEWS_FILE_NAME)
        self.assertEqual(Review.objects.count(), self.TEST_FILE_LINE_COUNT)

    def test_if_reviews_are_not_duplicated_when_creating(self):
        call_command('load_reviews_from_csv', self.relative_path + '/' + self.REVIEWS_FILE_NAME)
        reviews_count = Review.objects.count()
        call_command('load_reviews_from_csv', self.relative_path + '/' + self.REVIEWS_FILE_NAME)
        self.assertEqual(reviews_count, Review.objects.count())
