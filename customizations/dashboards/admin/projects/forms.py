from accounting import transactions
from horizon import exceptions
from horizon import forms


class GrantPromotionForm(forms.SelfHandlingForm):
    amount = forms.CharField(label='Amount')
    message = forms.CharField(label='Message to User')
    project_id = forms.CharField(label='project_id', widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        super(GrantPromotionForm, self).__init__(request, *args, **kwargs)

    def clean_amount(self):
        if not self.cleaned_data['amount'].isnumeric():
            raise forms.ValidationError('Amount must be numeric')
        return int(self.cleaned_data['amount'])

    def handle(self, request, data):
        try:
            transactions.UserTransactions().grant_user_promotion(
                data['project_id'],
                data['amount'],
                data['message'])
        except Exception:
            exceptions.handle(request, u'failed to grant project promotion')
        return True
