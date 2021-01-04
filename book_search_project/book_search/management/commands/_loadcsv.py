import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

from book_search.models import Book, Author, Type, Review


class BaseCSVCommand(BaseCommand):

    help = ''

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str, help="csv file path")

    def handle(self, *args, **options):
        file_path: str = options['file_path'][0]
        self._handle_file(file_path)

    def _handle_file(self, file_path: str):
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                self.handle_file_row(row)
            self.stdout.write('Grant')
        self.success_msg()

    def handle_file_row(self, row):
        raise NotImplementedError("handle_file_row is not implemented")

    def success_msg(self):
        pass

