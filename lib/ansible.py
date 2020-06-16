import os
import pulumi
import pulumi.dynamic
from typing import Any, Optional


class AnsibleInventoryProvider(pulumi.dynamic.ResourceProvider):

    current_content_ver = 1

    def create(self, props):
        hosts = props['hosts']
        with open(props['path'], 'w') as f:
            for host in hosts:
                f.write(f"{host['name']} ansible_host={host['ip']} ansible_user=core\n")

        out = {'hosts': props['hosts'], 'path': props['path'], 'content_ver': self.current_content_ver}
        return pulumi.dynamic.CreateResult(id_="foo", outs=out)

    def diff(self, resource_id, old_outputs, new_inputs):
        changes = False
        replaces = []

        if old_outputs['hosts'] != new_inputs['hosts']:
            changes = True
            replaces.append('hosts')

        if old_outputs['path'] != new_inputs['path']:
            changes = True
            replaces.append('path')

        if old_outputs.get('content_ver', 0) != self.current_content_ver:
            changes = True
            replaces.append('provider_template')

        return pulumi.dynamic.DiffResult(
                changes=changes, replaces=replaces, delete_before_replace=True
        )

    def update(self, resource_id, old_inputs, new_inputs):
        if old_inputs['path'] != new_inputs['path']:
            os.remove(old_inputs['path'])
        return self.create(new_inputs)


class AnsibleInventory(pulumi.dynamic.Resource):
    def __init__(self, name: str, props: Any, opts: Optional[pulumi.ResourceOptions] = None):
        if isinstance(props['hosts'], list):
            _hosts = []
            for host in props['hosts']:
                _hosts.append({'name': host.name, 'ip': host.access_ip_v4})
        else:
            assert False, "Unsupported"

        props['hosts'] = _hosts

        super().__init__(AnsibleInventoryProvider(), name, props, opts)
