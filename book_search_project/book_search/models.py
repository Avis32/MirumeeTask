from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=256)

    def __str__(self):
        return self.full_name


class Type(models.Model):
    type_name = models.CharField(max_length=256, null=False, primary_key=True, unique=True)

    def __str__(self):
        return self.type_name


class Book(models.Model):
    isbn = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=1024)
    author = models.ForeignKey(Author, related_name='books', null=False, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, related_name='books', on_delete=models.CASCADE)


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    review = models.CharField(max_length=512)
