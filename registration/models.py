from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from registration.managers import UserManager


class User(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=False,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    company = models.CharField(max_length=64, unique=True, blank=False)
    keystone_id = models.CharField(max_length=64, unique=False, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company']

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User
        """
        send_mail(subject, message, from_email, [self.email])

    def set_company(self, company):
        """
        Set company name
        """
        self.company = company

    def get_company(self):
        """
        Return company name
        """
        return self.company
