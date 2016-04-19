from django.db import models
import re

class Interface(models.Model):
    interface_name = models.CharField(max_length=255)
    interface_description = models.TextField()
    dhcp = models.BooleanField()
    mac_address = models.CharField(max_length=255, null=True, blank=True)
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    netmask = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    gateway_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    dns_servers = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):

        # validate dns_servers
        ips = self.dns_servers.split(" ")
        for ip in ips:
            if not re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip):
                raise Exception("IP address %s bad format" % ip)
        super(Interface, self).save(*args, **kwargs)




