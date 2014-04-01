from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from async.tasks import AsyncTasks


class CompanyAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        company = data.get('company')
        user_field(user, 'company', company)
        AsyncTasks.save_user.apply_async(kwargs={
            'company': data['company'],
            'user_name': data['email'],
            'password': data['password1'],
        }, link=AsyncTasks.update_keystone_id.s(data['email']))

        return super(CompanyAdapter, self).save_user(request, user,
                                                     form, commit)

    def confirm_email(self, request, email_address):
        AsyncTasks.email_confirmed.apply_async((email_address.email,))
        super(CompanyAdapter, self).confirm_email(request, email_address)

    def add_message(self, request, level, message_template,
                    message_context={}, extra_tags=''):
        pass
