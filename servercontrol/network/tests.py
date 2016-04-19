from django.test import TestCase
from network.models import Interface


class InterfaceTestCase(TestCase):
    def setUp(self):
        i = Interface.objects.create(interface_name="eth0", interface_description="Testinterface", dhcp=True)

    def test_dhcp(self):
        interface = Interface.objects.get(interface_name='eth0')
        interface.save()



