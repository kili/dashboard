from django import forms as forms
from billing_app.models import KopoKopoTransaction


class KopoKopoForm(forms.ModelForm):
    transaction_timestamp = forms.DateTimeField(required=True,
        input_formats=['%Y-%m-%dT%H:%M:%SZ'])
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)

    class Meta:
        model = KopoKopoTransaction
        fields = '__all__'

    def clean_sender_phone(self):
        return self.cleaned_data['sender_phone'].replace('+254', '0')
