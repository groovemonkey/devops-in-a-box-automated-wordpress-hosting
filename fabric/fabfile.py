# Fabfile for common administration tasks
from fabric.api import run, sudo, put, prompt, cd, env, get, task
from fabric.operations import local as lrun
from fabric.contrib.files import append
import os
import googleapiclient



@task
def create_instance():
    """Spin up compute instance from base image."""
    env.run = lrun
    env.hosts = ['localhost']

    # Initialize
    compute = googleapiclient.discovery.build('compute', 'v1')



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









