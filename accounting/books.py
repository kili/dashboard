from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from swingtix.bookkeeper.models import BookSet


class BookManager():

    def __init__(self):
        self.books = settings.ACCOUNTING_BOOKS,

    def get_book(self, currency='USD'):
        if not currency in self.books:
            raise Exception(u"no book for currency '{0}'".format(currency))
        try:
            self.book = BookSet.objects.get(description=self.books[currency])
        except ObjectDoesNotExist:
            self.book = BookSet(description=self.books[currency])
            self.book.save()
        return self.book
