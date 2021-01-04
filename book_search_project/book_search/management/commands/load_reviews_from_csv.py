from book_search.management.commands._loadcsv import BaseCSVCommand
from book_search.models import Book, Review


class Command(BaseCSVCommand):
    help = 'load Reviews from csv file'

    def handle_file_row(self, row):
        isbn, score, review = row[0].rstrip(';').split(';')
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist as e:
            self.stderr('Book with isbn: {isbn} Does Not Exists'.format(isbn=isbn))
        review, created = Review.objects.get_or_create(book=book, review=review, score=score)
        if created:
            self.stdout.write('created review {}'.format(review.id))
        else:
            self.stdout.write('review with id:{} already exists'.format(review.id))
