import pulumi
from pulumi_openstack import compute, blockstorage
from lib import create_ignition_config


def Host(hostname: str, domain: str, spec: dict) -> compute.Instance:
    custom_spec = spec.copy()
    custom_spec['name'] = hostname
    custom_spec['user_data'] = create_ignition_config(
            fqdn=f"{hostname}.{domain}",
            container_type='containers'  # 'containers' for podman, 'docker' for ...
    )

    # Create an OpenStack resource (Compute Instance)
    instance = compute.Instance(hostname, **custom_spec)
    pulumi.export(f'{hostname}_ip', instance.access_ip_v4)

    volume = blockstorage.Volume(f"{hostname}-data", size=40)
    compute.VolumeAttach(
            f"va-{hostname}-data",
            instance_id=instance.id,
            volume_id=volume.id,
            opts=pulumi.ResourceOptions(parent=instance)
    )

    return instance
