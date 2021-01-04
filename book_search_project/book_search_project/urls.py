from django.urls import path


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from book_search.views import book_list_view, book_detail_view

urlpatterns = [
    path('books/search/', book_list_view),
    path('books/<int:isbn>/', book_detail_view)
]
