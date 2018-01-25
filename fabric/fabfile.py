# Fabfile for common administration tasks
from fabric.api import run, sudo, put, prompt, cd, env, get, task
from fabric.operations import local as lrun
from fabric.contrib.files import append
import os
from googleapiclient import discovery
import pdb



@task
def create_instance(project, zone, region, name, machinetype="n1-standard-1", serviceacct_email="default", metadata={}):
    """
    Create a compute instance in the supplied project/zone, using the supplied
    machine type
    disk image
    metadata

    ## If we want to use a startup script to write nginx configs and set up the website
    # Is this run on each boot, or just on first startup during provisioning?
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), '../scripts/startup-script.sh'), 'r').read()

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
    compute = discovery.build('compute', 'v1')

    # Configure the machine
    machine_type = "zones/{}/machineTypes/{}".format(zone, machinetype)

    image_response = compute.images().getFromFamily(project=project, family='wordpress-base').execute()
    source_disk_image = image_response['selfLink']

    config = {
        'name': name,
        "zone": zone,
        'machineType': machine_type,
        "minCpuPlatform": "Automatic",

        "tags": {
          "items": [
            "http-server"
          ]
        },

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                "type": "PERSISTENT",
                'boot': True,
                'mode': "READ_WRITE",
                'autoDelete': True,
                "deviceName": name,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                    "diskSizeGb": "10",
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        "networkInterfaces": [
          {
            "subnetwork": "projects/%s/regions/%s/subnetworks/default" % (project, region),
            "accessConfigs": [
              {
                "name": "External NAT",
                "type": "ONE_TO_ONE_NAT"
              }
            ],
            "aliasIpRanges": []
          }
        ],

        "scheduling": {
          "preemptible": False,
          "onHostMaintenance": "MIGRATE",
          "automaticRestart": True
        },

        "deletionProtection": False,

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': serviceacct_email,
            'scopes': [
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/logging.write",
                "https://www.googleapis.com/auth/monitoring.write",
                "https://www.googleapis.com/auth/servicecontrol",
                "https://www.googleapis.com/auth/service.management.readonly",
                "https://www.googleapis.com/auth/trace.append"
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': metadata
    }

    success = compute.instances().insert(project=project, zone=zone, body=config).execute()
    print success
    return


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


@task
def list_instances(project, zone):
    """
    TODO: this does not work currently, even though it's taken from the docs
    here: https://cloud.google.com/compute/docs/tutorials/python-guide
    """
    env.run = lrun
    env.hosts = ['localhost']

    # Initialize
    compute = discovery.build('compute', 'v1')
    result = compute.instances().list(project=project, zone=zone).execute()
    pdb.set_trace()
    print(result)

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

