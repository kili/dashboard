from allauth.account import forms as allauth_forms
from django import forms as django_forms
from django.utils.translation import ugettext_lazy as _
from registration.models import User


class RegistrationForm(allauth_forms.SignupForm):

    company = django_forms.CharField(label=_("Company"),
        min_length=5,
        widget=django_forms.TextInput(
            attrs={'placeholder': _('Company Name'),
               'autofocus': 'autofocus'}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        email_label = _('Email')
        self.fields["email"].label = email_label
        self.fields["email"].widget.attrs.update({'placeholder': email_label})

    def clean_company(self):
        company = self.cleaned_data["company"]
        try:
            User.objects.get(company=company)
            raise django_forms.ValidationError(
                "The company name you provided is already in use.")
        except User.DoesNotExist:
            return company

    def save(self, user):
        pass


class ResetPasswordForm(allauth_forms.ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        email_label = _('Email')
        self.fields["email"].label = email_label
        self.fields["email"].widget.attrs.update({'placeholder': email_label})
