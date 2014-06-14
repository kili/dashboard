import datetime
from horizon import forms


class DateRangeForm(object):

    def __init__(self, request):
        self.request = request

    def get_date_range(self):
        if not hasattr(self, 'start') or not hasattr(self, 'end'):
            self.set_range()
        return (self.start, self.end)

    def set_range(self):
        form = self.get_form()
        if form.is_valid():
            self.start = form.cleaned_data['start']
            self.end = form.cleaned_data['end']
        else:
            self.init_form()

    def get_form(self):
        if not hasattr(self, 'form'):
            if any(key in ['start', 'end'] for key in self.request.GET):
                self.form = forms.DateForm(self.request.GET)
            else:
                self.form = forms.DateForm(initial=self.init_form())
        return self.form

    def init_form(self):
        today = datetime.date.today()
        self.start = datetime.date(day=1, month=today.month, year=today.year)
        self.end = datetime.date.today()
        return {'start': self.start, 'end': self.end}
