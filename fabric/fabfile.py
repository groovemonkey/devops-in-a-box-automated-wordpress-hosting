# Fabfile for common administration tasks
from fabric.api import run, sudo, put, prompt, cd, env, get, task
from fabric.operations import local as lrun
from fabric.contrib.files import append
import os
import googleapiclient



@task
def create_instance(project, zone, name, machinetype="n1-standard-1", source_disk_image="", metadata={}):
    """
    Create a compute instance in the supplied project/zone, using the supplied
    machine type
    disk image
    metadata

    # Sample metadata dict
    metadata = {
        'items': [{
            # Startup script is automatically executed by the
            # instance upon startup.
            'key': 'startup-script',
            'value': startup_script
        }]
    }
    """
    env.run = lrun
    env.hosts = ['localhost']

    # Initialize
    compute = googleapiclient.discovery.build('compute', 'v1')

    # Configure the machine
    machine_type = "zones/{}/machineTypes/{}".format(zone, machinetype)

    # TODO: are we doing this here?
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script.sh'), 'r').read()

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': metadata
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


# @task
# def create_site_db(dbname):
#     """Create a DB user on the cluster."""
#     env.run = lrun
#     env.hosts = ['localhost']
#     # TODO: check if this DB already exists?
#     # Create the DB
#     run('mysql -h %s -u %s -p%s -e "CREATE DATABASE IF NOT EXISTS %s"' %
#             (DB_HOST, DB_USER, DB_PASSWORD, dbname))
#     pass


@task
def create_site_user(dbname, dbuser, dbpassword):
    """Create a site DB and a DB user on the cluster."""
    env.run = lrun
    env.hosts = ['localhost']
    # TODO: check if this user already exists?
    # Create the user
    run('mysql -h %s -u %s -p%s -e "CREATE DATABASE %s; GRANT ALL PRIVILEGES ON %s.* TO %s@localhost IDENTIFIED BY %s; FLUSH PRIVILEGES;"' %
            (DB_HOST, DB_USER, DB_PASSWORD, dbname, dbname, dbuser, dbpassword))
    pass


def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']


@task
def create_wp_config():
    """Create a wp-config.php file from site metadata (hostname, mysql auth/endpoint info, etc.)."""
    pass


@task
def list_active_sites():
    """List active sites."""
    pass


@task
def backup_site_db():
    """Back up mysql DB."""
    pass


@task
def backup_site_files():
    """Back up WordPress site files."""
    pass


@task
def delete_instance(project, zone, name):
    """
    Delete a compute instance.
    """
    env.run = lrun
    env.hosts = ['localhost']
    
    # Initialize
    compute = googleapiclient.discovery.build('compute', 'v1')

    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()







