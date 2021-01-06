# Instalation
```
pip install -r requirements.txt
```

# Loading data from .csv file
## 1.Load Books
Loading books is done with _load_books_from_csv_ command
```
python manage.py load_books_from_csv <path_to_file>
```
## 2.Loading Reviews 
Loading Reviews is simmiliar to loading books with _load_reviews_from_csv_ command
```
python manage.py load_reviews_from_csv <path_to_file>
```

# Endpoints
##1.Book Search
endpoint url:

`/books/search/`

endpoint query params:

* **q** - full title or start of the title to search book with case-insensitive

* **page** - page number for results that exceeds 10 results returned(if it's not passed 0 is used)

books are ordered by isbn number if `q` is not passed books are returned in that order

return results:
```
{
    "books": [
        {"isbn": int,
        "number": text,
        "author": {
            "id": number,
            "full_name": text
        },
        "type": text}
        ]
}
```

## 2.Book detail

endpoint url:

`/books/<book_isbn>/`

endpoint url params:

* **book_isbn** - book isbn

return results:
```
{
    "isbn": number,
    "title": text,
    "author": {
        "id": number,
        "full_name": text
        },
    "type": text,
    "reviews": [{
        "id": number,
        "score": number,
        "review": text}
        ]}
```


