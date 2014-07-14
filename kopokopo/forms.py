from django import forms as django_forms
from billing_app.models import K2RawData

class KopoKopoForm(django_forms.ModelForm):
    transaction_timestamp = django_forms.DateTimeField(required=True,
        input_formats=['%Y-%m-%dT%H:%M:%SZ'])

    class Meta:
        model = K2RawData
        fields = '__all__'

    def clean_sender_phone(self, 
