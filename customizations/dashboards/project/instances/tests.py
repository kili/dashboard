from django.core.urlresolvers import reverse
from django import http

from mox import IgnoreArg  # noqa
from mox import IsA  # noqa

from openstack_dashboard import api
from openstack_dashboard.api import cinder
from openstack_dashboard.test import helpers as test
from openstack_dashboard.usage import quotas

from customizations.dashboards.project.instances.workflows \
    import create_instance as customized_create_instance


class InstanceTests(test.TestCase):
    @test.create_stubs({api.glance: ('image_list_detailed',),
                        api.neutron: ('network_list',
                                      'profile_list',),
                        api.nova: ('extension_supported',
                                   'flavor_list',
                                   'keypair_list',
                                   'tenant_absolute_limits',
                                   'availability_zone_list',),
                        api.network: ('security_group_list',),
                        cinder: ('volume_list',
                                 'volume_snapshot_list',),
                        quotas: ('tenant_quota_usages',)})
    def test_launch_form_instance_count_error(self):
        flavor = self.flavors.first()
        image = self.images.first()
        server = self.servers.first()
        volume = self.volumes.first()
        sec_group = self.security_groups.first()
        avail_zone = self.availability_zones.first()
        customization_script = 'user data'
        device_name = u'vda'
        volume_choice = "%s:vol" % volume.id
        quota_usages = self.quota_usages.first()

        api.nova.extension_supported('BlockDeviceMappingV2Boot',
                                     IsA(http.HttpRequest)) \
                .AndReturn(True)
        api.nova.flavor_list(IsA(http.HttpRequest)) \
                .AndReturn(self.flavors.list())
        api.nova.keypair_list(IsA(http.HttpRequest)) \
                .AndReturn(self.keypairs.list())
                #.AndReturn([])
        api.network.security_group_list(IsA(http.HttpRequest)) \
                .AndReturn(self.security_groups.list())
        api.nova.availability_zone_list(IsA(http.HttpRequest)) \
                .AndReturn(self.availability_zones.list())
        api.glance.image_list_detailed(IsA(http.HttpRequest),
                                       filters={'is_public': True,
                                                'status': 'active'}) \
                  .AndReturn([self.images.list(), False])
        api.glance.image_list_detailed(IsA(http.HttpRequest),
                            filters={'property-owner_id': self.tenant.id,
                                     'status': 'active'}) \
                  .AndReturn([[], False])
        api.neutron.network_list(IsA(http.HttpRequest),
                                 tenant_id=self.tenant.id,
                                 shared=False) \
                .AndReturn(self.networks.list()[:1])
        api.neutron.network_list(IsA(http.HttpRequest),
                                 shared=True) \
                .AndReturn(self.networks.list()[1:])
        # TODO(absubram): Remove if clause and create separate
        # test stubs for when profile_support is being used.
        # Additionally ensure those are always run even in default setting
        if api.neutron.is_port_profiles_supported():
            policy_profiles = self.policy_profiles.list()
            api.neutron.profile_list(IsA(http.HttpRequest),
                                     'policy').AndReturn(policy_profiles)
        cinder.volume_list(IsA(http.HttpRequest)) \
                .AndReturn(self.volumes.list())
        cinder.volume_snapshot_list(IsA(http.HttpRequest)).AndReturn([])

        api.nova.flavor_list(IsA(http.HttpRequest)) \
                .AndReturn(self.flavors.list())
        api.nova.tenant_absolute_limits(IsA(http.HttpRequest)) \
           .AndReturn(self.limits['absolute'])
        quotas.tenant_quota_usages(IsA(http.HttpRequest)) \
                .AndReturn(quota_usages)
        api.nova.flavor_list(IsA(http.HttpRequest)) \
                .AndReturn(self.flavors.list())

        self.mox.ReplayAll()

        form_data = {'flavor': flavor.id,
                     'source_type': 'image_id',
                     'image_id': image.id,
                     'availability_zone': avail_zone.zoneName,
                     'keypair': '',
                     'name': server.name,
                     'customization_script': customization_script,
                     'project_id': self.tenants.first().id,
                     'user_id': self.user.id,
                     'groups': sec_group.name,
                     'volume_type': 'volume_id',
                     'volume_id': volume_choice,
                     'device_name': device_name,
                     'count': 1}
        url = reverse('horizon:project:instances:launch')
        res = self.client.post(url, form_data)

        for context in [l2_context
                        for l1_context in res.context
                        for l2_context in l1_context
                        if 'form' in l2_context
                        and l2_context['form'].__class__
                        == customized_create_instance.
                        CustomSetAccessControlsAction]:
            self.assertEqual(context['form'].is_valid(), False)
