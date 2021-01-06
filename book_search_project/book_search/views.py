from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse


from book_search.models import Book, Review


class BookSerializer:
    def __init__(self, book: Book):
        self.book: Book = book

    def serialize(self):
        book = self.book
        return {
            'isbn': book.isbn,
            'title': book.title,
            'author': {
                'id': book.author.id,
                'full_name': book.author.full_name
            },
            'type': str(book.type)
        }


def book_list_view(request, **kwargs):
    books_page_size: int = 10
    query = request.GET.get('q')
    books = Book.objects.all().order_by('isbn')
    if query:
        books = books.filter(title__istartswith=query)
    paginator = Paginator(books, books_page_size)
    page_number = request.GET.get('page', 0)
    page_obj = paginator.get_page(page_number)
    page_obj = [BookSerializer(instance).serialize() for instance in page_obj]
    return JsonResponse({'books': page_obj})


def book_detail_view(request, isbn, **kwargs):
    book = Book.objects.get(isbn=isbn)
    reviews = Review.objects.filter(book=book)
    book = BookSerializer(book).serialize()
    book['reviews'] = [model_to_dict(instance, exclude=['book']) for instance in reviews]
    return JsonResponse(book)
