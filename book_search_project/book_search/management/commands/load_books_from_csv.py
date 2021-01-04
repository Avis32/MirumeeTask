from book_search.management.commands._loadcsv import BaseCSVCommand
from book_search.models import Author, Type, Book


class Command(BaseCSVCommand):
    help = 'load Books from csv file'

    def handle_file_row(self, row):
        isbn, title, author_name, type_name = row[0].rstrip(';').split(';')
        author, author_created = Author.objects.get_or_create(full_name=author_name)
        book_type, type_created = Type.objects.get_or_create(type_name=type_name)
        book, book_created = Book.objects.get_or_create(isbn=isbn, author=author, title=title, type=book_type)
        if author_created:
            self.stdout.write('created author {}'.format(author.full_name))
        else:
            self.stdout.write('author {} already exists'.format(author.full_name))
        if type_created:
            self.stdout.write('created book_type {}'.format(book_type.type_name))
        else:
            self.stdout.write('book_type {} already exists'.format(book_type.type_name))
        if book_created:
            self.stdout.write('created book {}'.format(book.title))
        else:
            self.stdout.write('book {} already exists'.format(book.title))
