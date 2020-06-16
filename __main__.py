"""An OpenStack Python Pulumi program"""
import os

from lib import AnsibleInventory
from resources import Host

assert os.environ['OS_PROJECT_NAME'] == 'PROJECT'

base_instance_spec = dict(
            flavor_name='m1.small',
            image_name='fcos-31-20200223',
            networks=[{'name': 'netname'}],
            security_groups=['egress-all', 'icmp-all', 'admin-ssh'],
)


host = Host("hostname", "domain.fi", base_instance_spec)
AnsibleInventory("inventory", {'path': '../ansible/inventory', 'hosts': [host]})
