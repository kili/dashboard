import base64
from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend  # noqa
from django.contrib.auth import get_user_model  # noqa
from django.contrib.auth.middleware import RemoteUserMiddleware  # noqa


class K2UserMiddleware(RemoteUserMiddleware):
    header = settings.K2_AUTHORIZATION_HEADER


class K2AuthBackend(RemoteUserBackend):

    def authenticate(self, remote_user=None):
        if not remote_user:
            return None

        # decode credentials
        credentials = base64.b64decode(
            remote_user.replace('Basic ', '')).split(':')

        if not credentials:
            return None

        UserModel = get_user_model()
        password = credentials[1]

        try:
            user = UserModel.objects.get(
                email=credentials[0],
                company='KopoKopo_K2'
            )
            if user.check_password(password):
                return self.configure_user(user)
        except UserModel.DoesNotExist:
            pass

    def configure_user(self, user):
        return user
