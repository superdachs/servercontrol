from django.db import models
import re
import netifaces
import os

CONFIG_PATH = os.path.join('/', 'etc', 'netctl', 'interfaces')





class Interface(models.Model):
    interface_name = models.CharField(max_length=255)
    interface_description = models.TextField()
    dhcp = models.BooleanField(default=False)
    mac_address = models.CharField(max_length=255, null=True, blank=True)
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    netmask = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    gateway_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    dns_servers = models.TextField(null=True, blank=True)
    routes = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    connection = models.CharField(max_length=255, default="ethernet")

    def __str__(self):
        if self.dhcp:
            dhcp = "DHCP"
        else:
            dhcp = "STATIC"
        if self.active:
            active = "ACTIVE"
        else:
            active = "INACTIVE"
        return self.interface_name + " - " + self.mac_address + " - " + self.ipv4_address + " - " + dhcp + " - " + active


    def save(self, *args, **kwargs):

        # validate dns_servers
        if self.dns_servers:
            ips = self.dns_servers.split(" ")
            for ip in ips:
                if not re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip):
                    raise Exception("IP address %s bad format" % ip)
        # save to database
        super(Interface, self).save(*args, **kwargs)

        # save configfile
        configfile_path = os.path.join(CONFIG_PATH, self.interface_name)
        with open(configfile_path, 'w') as configfile:
            configfile.write("Description='%s'\n" % self.interface_description)
            configfile.write("Interface=%s\n" % self.interface_name)
            configfile.write("Connection=%s\n" % self.connection)
            if self.dhcp:
                configfile.write("IP=%s\n" % "dhcp")
            else:
                configfile.write("IP=%s\n" % "static")




class Tools:
    # get network interfaces from system
    def get_ifaces_from_system(self):
        interfaces = {}
         
        for interface in netifaces.interfaces():
            
            mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            description = "none"
            ipv4_address = "0.0.0.0"
            ipv4_netmask = "0.0.0.0"
            ipv4_gateway = "0.0.0.0"
            dhcp = False
            active = False
            
            

            try:
                with open(os.path.join(CONFIG_PATH, interface), 'r') as configfile:
                    pass
            except FileNotFoundError:
                print("Config file not found!")
                pass

            print('found interface: %s' % interface)
            interfaces.update({interface: {"description": description, "mac": mac, "dhcp": dhcp, "ipv4_address": ipv4_address, "ipv4_netmask": ipv4_netmask, "ipv4_gateway": ipv4_gateway, 'active': active}})

        return interfaces


    def sync_ifaces_to_db(self, interfaces_sys):

        for interface_sys in interfaces_sys:
            print("syncing interface %s to db" % interface_sys)
            try:
                interface_db = Interface.objects.get(mac_address=interfaces_sys[interface_sys]['mac'])
            except Interface.DoesNotExist:
                interface_db = Interface()

            interface_db.interface_name = interface_sys
            interface_db.interface_description = interfaces_sys[interface_sys]['description']
            interface_db.dhcp = interfaces_sys[interface_sys]['dhcp']
            interface_db.mac_address = interfaces_sys[interface_sys]['mac']
            interface_db.ipv4_address = interfaces_sys[interface_sys]['ipv4_address']
            interface_db.netmask = interfaces_sys[interface_sys]['ipv4_netmask']
            interface_db.gateway_address = interfaces_sys[interface_sys]['ipv4_gateway']
            interface_db.dns_servers = None
            interface_db.routes = None
            interface_db.active = interfaces_sys[interface_sys]['active']
            interface_db.connection = "ethernet"

            interface_db.save()

    def remove_old_interfaces_from_db(self, interfaces_sys):
        for interface_db in Interface.objects.all():
            if not interface_db.interface_name in interfaces_sys:
                interface_db.delete()
