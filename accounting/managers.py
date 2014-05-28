from django.conf import settings
from django.core import exceptions
import re
from swingtix.bookkeeper.models import Account
from swingtix.bookkeeper.models import BookSet


class BookManager():

    def __init__(self):
        self.books = settings.ACCOUNTING_BOOKS

    def get_book(self, currency='USD'):
        if currency not in self.books:
            raise Exception(u"no book for currency '{0}'".format(currency))
        try:
            self.book = BookSet.objects.get(description=self.books[currency])
        except exceptions.ObjectDoesNotExist:
            self.book = BookSet(description=self.books[currency])
            self.book.save()
        return self.book


class AccountManager():

    def __init__(self):
        self.valid_accounts = settings.ACCOUNTING_ASSET_SOURCES
        self.valid_accounts.append(settings.ACCOUNTING_PROMOTIONS_ACCOUNT)
        self.valid_accounts.append(settings.ACCOUNTING_REVENUE_ACCOUNT)
        self.valid_accounts.append(
            settings.ACCOUNTING_USER_ACCOUNT_FORMAT["regex"])

        # accounts where credit and debit are negated
        self.credit_negative_accounts = settings.ACCOUNTING_ASSET_SOURCES
        self.credit_negative_accounts.append(
            settings.ACCOUNTING_PROMOTIONS_ACCOUNT)

    def name_is_valid(self, account_name):
        if re.match(
                "(" + ")|(".join(self.valid_accounts) + ")",
                account_name):
            return True
        return False

    def format_user_account(self, user):
        return settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(user)

    def is_credit_positive(self, account_name):
        if account_name in self.credit_negative_accounts:
            return False
        return True

    def create_account(self, account_name):
        account = Account(
            bookset=BookManager().get_book(),
            name=account_name,
            positive_credit=self.is_credit_positive(account_name))
        account.save()
        return account

    def is_asset_source(self, account):
        if account in settings.ACCOUNTING_ASSET_SOURCES:
            return True
        return False

    def get_account(self, account_name):
        if not self.name_is_valid(account_name):
            raise Exception(u"account name '{0}' is not valid"
                            .format(account_name))
        book = BookManager().get_book()
        try:
            return book.get_account(account_name)
        except exceptions.ObjectDoesNotExist:
            return self.create_account(account_name)

    def get_user_account(self, user):
        return self.get_account(self.format_user_account(user))

    def get_revenue_account(self):
        return self.get_account(settings.ACCOUNTING_REVENUE_ACCOUNT)

    def get_promotions_account(self):
        return self.get_account(settings.ACCOUNTING_PROMOTIONS_ACCOUNT)
