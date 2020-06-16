import subprocess
import jinja2

def create_ignition_config(**variables) -> str:
    with open('templates/config.fcc.j2', 'r') as f:
        template = f.read()
        fcc = jinja2.Template(template).render(**variables)
    return subprocess.check_output(['podman', 'run', '-i', '--rm', 'quay.io/coreos/fcct:v0.5.0', '--pretty', '--strict'], input=fcc.encode()).decode()
