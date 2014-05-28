from accounting import books
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import re
from swingtix.bookkeeper.models import Account


class AccountManager():

    def __init__(self):
        self.valid_accounts = settings.ACCOUNTING_ASSET_SOURCES
        self.valid_accounts.append(settings.ACCOUNTING_PROMOTIONS_ACCOUNT)
        self.valid_accounts.append(settings.ACCOUNTING_REVENUE_ACCOUNT)
        self.valid_accounts.append(settings.ACCOUNTING_USER_ACCOUNT_FORMAT)

        # accounts where credit and debit are negated
        self.credit_negative_accounts = settings.ACCOUNTING_ASSET_SOURCES

    def name_is_valid(self, account_name):
        if re.match(
                "(" + ")|(".join(self.valid_accounts) + ")",
                account_name):
            return True
        return False

    def is_credit_positive(self, account_name):
        if account_name in self.credit_negative_accounts:
            return False
        return True

    def get_account(self, account_name):
        if not self.name_is_valid(account_name):
            raise Exception(u"account name '{0}' is invalid"
                            .format(account_name))
        book = books.BookManager().get_book()
        try:
            return book.get_account(account_name)
        except ObjectDoesNotExist:
            account = Account(
                bookset=book,
                name=account_name,
                positive_credit=self.is_credit_positive(account_name))
            account.save()
            return account
