from allauth.account import adapter
from allauth.account import utils
from async.tasks import AsyncTasks


class CompanyAdapter(adapter.DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        company = data.get('company')
        utils.user_field(user, 'company', company)
        AsyncTasks.save_user.apply_async(kwargs={
            'company': data['company'],
            'user_name': data['email'],
            'password': data['password1'],
            'email': data['email'],
        }, link=AsyncTasks.update_keystone_id.s(data['email']))

        return super(CompanyAdapter, self).save_user(request, user,
                                                     form, commit)

    def confirm_email(self, request, email_address):
        AsyncTasks.email_confirmed.apply_async((email_address.email,))
        super(CompanyAdapter, self).confirm_email(request, email_address)

    def add_message(self, request, level, message_template,
                    message_context={}, extra_tags=''):
        pass

    def set_password(self, user, password):
        AsyncTasks.set_password.apply_async(kwargs={
            'user': user.get_username(),
            'password': password})
        return super(CompanyAdapter, self).set_password(user, password)
