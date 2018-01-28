# Functions that might be useful for fab tasks

import subprocess
import re



def clean_domain(domain):
    # TODO: Implement this in a serious way
    re.sub("\.","-", domain)
    return domain


def create_wp_config_string(WPSite):
    """
    Create a wp config multiline string (template) from a WPSite object.
    """
    salts = subprocess.check_output(["curl", "https://api.wordpress.org/secret-key/1.1/salt/"])
    configstring = f'''
<?php
define('DB_NAME', {WPSite.dbname});
define('DB_USER', {WPSite.dbuser});
define('DB_PASSWORD', {WPSite.dbpass});
define('DB_HOST', {WPSite.dbhost});
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');

{salts}

$table_prefix  = 'wp_';
define('WP_DEBUG', false);

if ( !defined('ABSPATH') )
    define('ABSPATH', dirname(__FILE__) . '/');

require_once(ABSPATH . 'wp-settings.php');

    '''
    return configstring


def pretty_print_droplet_data(droplet):
    """
    Takes a droplet object (from the 'digitalocean' library) and returns a 
    nicely formatted string of attributes.
    """
    drop_info = f'''

name: {droplet.name}
status: {droplet.status}
ip_address: {droplet.ip_address}
memory: {droplet.memory}
vcpus: {droplet.vcpus}
disk: {droplet.disk}

Region: {droplet.region['name']}
Distro: {droplet.image['distribution']}

Hourly Price: {droplet.size['price_hourly']}
Monthly Price: {droplet.size['price_monthly']}

ssh_keys: {droplet.ssh_keys}
user_data: {droplet.user_data}
Tags: {droplet.tags}
id: {droplet.id}
created_at: {droplet.created_at}

    '''
    return drop_info


