from django.conf.urls import patterns, url
from custom.dashboards.project.instances.views import CustomLaunchInstanceView

urlpatterns = patterns(
    url(r"^project/instances/launch/$",
        CustomLaunchInstanceView,
        name="custom_launch_instance_view"),
)
