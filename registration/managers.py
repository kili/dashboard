from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, company=None):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(email=self.normalize_email(email),)
        user.set_company(company)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, company=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            company=company,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
