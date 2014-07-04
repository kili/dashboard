from accounting import managers
from customizations.dashboards.admin.projects import tables
from customizations.dashboards.admin.projects import forms as project_forms
from django.core import urlresolvers
from horizon import forms
from openstack_dashboard.dashboards.admin.projects import views


class CustomIndexView(views.IndexView):
    table_class = tables.CustomTenantsTable

    def get_data(self, *args, **kwargs):
        am = managers.AccountManager()
        data = super(CustomIndexView, self).get_data(*args, **kwargs)
        for obj in data:
            setattr(obj,
                    'balance',
                    am.get_user_account(obj.id).balance())
        return data


class GrantPromotionView(forms.ModalFormView):
    form_class = project_forms.GrantPromotionForm
    template_name = 'admin/projects/promotion.html'
    success_url = urlresolvers.reverse_lazy('horizon:admin:projects:index')

    def get_context_data(self, **kwargs):
        return dict(
            super(GrantPromotionView, self).get_context_data(**kwargs).items() +
                  [('promotion', {'project_id': self.kwargs['project_id']})])

    def get_initial(self):
        return {'project_id': self.kwargs['project_id']}
