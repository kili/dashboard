from customizations.dashboards.project.instances.workflows \
    import create_instance as customized_create_instance
from django.conf import urls
from openstack_dashboard.dashboards.project.instances import urls as inst_urls


class LaunchInstanceViewCustomizer:

    def execute(self):
        """insert our own launch instance view into urls before the
           openstack_dashboard one
        """
        inst_urls.urlpatterns.insert(0, urls.url(
            r'^launch$',
            customized_create_instance.CustomLaunchInstanceView.as_view(),
            name='launch'))
