from __future__ import absolute_import
from django.conf import settings
from keystoneclient.v2_0.client import Client
from allauth.account.utils import user_field
from keystone_wrapper.transactions import CreateUserTransaction
from registration.models import User
from .celery import celery_app


class AsyncTasks():

    @celery_app.task
    def email_confirmed(address):
        keystone_id = User.objects.get_by_natural_key(address).keystone_id
        client = Client(token=settings.KEYSTONE_TOKEN,
                        endpoint=settings.KEYSTONE_URL)
        client.users.update(keystone_id, enabled=True)

    @celery_app.task
    def update_keystone_id(keystone_id, address):
        user = User.objects.get_by_natural_key(address)
        user_field(user, 'keystone_id', keystone_id)
        user.save()

    @celery_app.task
    def save_user(company, user_name, password):
        (tenant_id, user_id) = CreateUserTransaction().create_user(
            user_name=user_name,
            password=password,
            group_name=settings.KEYSTONE_DEFAULT_GROUP,
            tenant_name=company,
        )

        if not user_id:
            raise Exception("couldn't create keystone user")

        return user_id
