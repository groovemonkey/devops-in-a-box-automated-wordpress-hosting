

def create_instance(compute, project, zone, name, machinetype="n1-standard-1", source_disk_image="", metadata):
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



def delete_instance(compute, project, zone, name):
    """
    Delete a compute instance.
    """
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()



def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']



