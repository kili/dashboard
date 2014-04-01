from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import User


class RegistrationForm(forms.Form):

    company = forms.CharField(label=_("Company"),
                              min_length=5,
                              widget=forms.TextInput(
                                  attrs={'placeholder': _('Company Name'),
                                         'autofocus': 'autofocus'}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_company(self):
        company = self.cleaned_data["company"]
        try:
            User.objects.get(company=company)
            raise forms.ValidationError("The company name you provided"
                                        " is already in use.")
        except User.DoesNotExist:
            return company

    def save(self, user):
        pass
