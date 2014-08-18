from __future__ import absolute_import
from allauth.account import utils
from async.celery import celery_app
from django.conf import settings
from keystone_wrapper.transactions import CreateUserTransaction
from keystone_wrapper.client import KeystoneClient
from registration.models import User


class AsyncTasks():

    @celery_app.task
    def email_confirmed(address):
        KeystoneClient.get_client().users.update(
            User.objects.get_by_natural_key(address).keystone_id,
            enabled=True)

    @celery_app.task
    def update_keystone_id(keystone_id, address):
        user = User.objects.get_by_natural_key(address)
        utils.user_field(user, 'keystone_id', keystone_id)
        user.save()

    @celery_app.task
    def save_user(company, user_name, password, email):
        (tenant_id, user_id) = CreateUserTransaction().create_user(
            user_name=user_name,
            password=password,
            group_name=settings.KEYSTONE_DEFAULT_GROUP,
            tenant_name=company,
            email=email,
        )

        if not user_id:
            raise Exception("couldn't create keystone user")

        return user_id

    @celery_app.task
    def set_password(user, password):
        KeystoneClient.get_client().users.update_password(
            User.objects.get_by_natural_key(user).keystone_id,
            password)
