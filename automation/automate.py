# Common administration tasks
import os
import digitalocean
from googleapiclient import discovery
import helpers
from WPSite import WPSite
from custom_ansible import TL_Ansible_Playbook
import argparse


DO_TOKEN = os.environ['DO_TOKEN']


def create_new_wp_site(wpsite):
    """
    Create a new wordpress site, using digitalocean for testing.
    Takes a WPSite object and provisions a WordPress site on a new host.
    """
    ## DIGITAL OCEAN
    newhost = create_digitalocean_instance()

    # Add a tag to the instance, e.g. tutorialinux.com
    tag_digitalocean_instance(newhost, wpsite.domain)

    ## ANSIBLE
    inventory_file = "TODO-mktemp-and-add-newhost.ip"
    dbvars = {
        'user': wpsite.dbuser,
        'password': wpsite.dbpassword,
        'database': wpsite.dbname,
        'dbhost': wpsite.dbhost
    }
    pb_mysql_setup = TL_Ansible_Playbook(playbook_path="ansible/mysql_new_site.yml", host_list=newhost, inventory_file=inventory_file, extravars=dbvars)
    mysql_success = pb_mysql_setup.run()
    return mysql_success


def tag_digitalocean_instance(droplet, tag):
    tag = digitalocean.Tag(token=DO_TOKEN, name=tag)
    tag.create() # create tag if not already created
    tag.add_droplets(droplet.id)


def create_digitalocean_instance():
    """
    Create a new DO droplet. Once the droplet is provisioned, return a droplet IP.
    """
    droplet = digitalocean.Droplet(token="secretspecialuniquesnowflake",
                                   name='Example',
                                   region='nyc2',
                                   image='debian-9-x64', # Debian 9.3
                                   size_slug='512mb',  # or '1gb'?
                                   backups=True)
    droplet.create()

    # Wait for provisioning to complete
    actions = droplet.get_actions()
    for action in actions:
        action.load()
        # Once it shows complete, droplet is up and running
        print(action.status)

    return droplet.ip_address


def list_digitalocean_instances():
    manager = digitalocean.Manager(token=DO_TOKEN)
    my_droplets = manager.get_all_droplets()

    for drop in my_droplets:
        print(helpers.pretty_print_droplet_data(drop))
    
    return my_droplets


def create_google_instance(project, zone, region, name, machinetype="n1-standard-1", serviceacct_email="default", metadata={}):
    """
    Create a compute instance in the supplied project/zone, using the supplied

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
    return success


# # def create_site_db(dbname):
#     """Create a DB user on the cluster."""
#     env.run = lrun
#     env.hosts = ['localhost']
#     # TODO: check if this DB already exists?
#     # Create the DB
#     run('mysql -h %s -u %s -p%s -e "CREATE DATABASE IF NOT EXISTS %s"' %
#             (DB_HOST, DB_USER, DB_PASSWORD, dbname))
#     pass


def create_site_user(dbname, dbuser, dbpassword):
    """Create a site DB and a DB user on the cluster."""
    # TODO: check if this user already exists?
    # Create the user
    # run('mysql -h %s -u %s -p%s -e "CREATE DATABASE %s; GRANT ALL PRIVILEGES ON %s.* TO %s@localhost IDENTIFIED BY %s; FLUSH PRIVILEGES;"' %
    #         (DB_HOST, DB_USER, DB_PASSWORD, dbname, dbname, dbuser, dbpassword))
    pass


def list_google_instances(project, zone):
    """
    TODO: this does not work currently, even though it's taken from the docs
    here: https://cloud.google.com/compute/docs/tutorials/python-guide
    """
    # Initialize
    compute = discovery.build('compute', 'v1')
    result = compute.instances().list(project=project, zone=zone).execute()
    print(result)

    return result['items']


def create_wp_config():
    """Create a wp-config.php file from site metadata (hostname, mysql auth/endpoint info, etc.)."""
    pass


def list_active_sites():
    """List active sites."""
    pass


def backup_site_db():
    """Back up mysql DB."""
    pass


def backup_site_files():
    """Back up WordPress site files."""
    pass


def delete_instance(project, zone, name):
    """
    Delete a compute instance.
    """
    # Initialize
    compute = googleapiclient.discovery.build('compute', 'v1')

    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command you want to run, e.g. add-site")
    parser.add_argument("--domain", help="domain for the new site")
    parser.add_argument("--dbname")
    parser.add_argument("--dbuser")
    parser.add_argument("--dbpass")
    parser.add_argument("--dbhost")
    # parser.add_argument("--cloud")
    parser.parse_args()

    # Have we implemented this command?
    if args.command not in ["add-site", "addsite"]:
        print("Command not implemented.")
        sys.exit()

    if args.command == "add-site":
        if not args.domain and args.dbname and args.dbuser and args.dbpass and args.dbhost and args.webhost and args.ip and args.cloud:
            print("Missing required argument. Please check your command and try again.")
            sys.exit()

        # Good to go -- create WPSite object
        domain = clean_domain(domain)
        wpsite = WPSite(dbhost=dbhost, dbname=dbname, dbuser=dbuser, dbpass=dbpass, domain=domain)
        create_new_wp_site(wpsite)

        # Print details of created machine/site -- TODO: make this much nicer
        print("New website has been created. Please remember the following details:\n")
        print(wpsite.__dict__)


if __name__ == '__main__':
    main()

