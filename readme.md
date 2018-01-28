# Automated WordPress (or other dynamic website) hosting


## Dave's TODO

1. Finish/test 'master instance' setup script (install-wordpress-hosting-base.sh)
1. Create a DO 'master' wp hosting image
1. create DigitalOcean MySQL master
1. Get the ansible test playbook working (called from automate.py)
1. automate.py --> implement "TODO-mktemp-and-add-newhost.ip"
1. flesh out admin tasks in automation code
    - move wp-config.php template creation from helpers.py to ansible
    - new instance setup script -- install and configure a single WP site -- scripts/set-up-wp-site.sh (pass it in as a startup script -- GCP-metadata or the analogous DO/AWS operation)

1. create GCP MySQL master


### DONE

- "I want a new site" --> create WPSite object --> automate.py/create_new_wp_site()



## Filming plan:

- Separate theory/skill and 'practical tutorial' videos, to make re-filming sections easier as API changes happen? Separate 'teaching' and 'showing.'




## AUTOMATION TODO


### Low-level Automation

These automation tasks map directly to implementation-specific concepts. They form the foundation for higher-level automation functions.

- Create a site DB user on the cluster
- Enable/Disable site (nginx stop)
- Create a wp-config.php file from site metadata (hostname, mysql auth/endpoint info, etc.)
- backup mysql db
- backup wp files
- update mysql credentials in wp-config.php


#### DONE

- list active sites
- Spin up compute instance from base image



### High-level automation

These automation functions map directly to the BUSINESS GOALS that our application carries out. They are composed of low-level, implementation-hiding functions. These high-level automation functions are called directly by our management scripts and fab tasks.

- Create new site (spin up base image, create site DB user, create a wp-config.php file)
- Update mysql endpoint for a site
- Back up site (list active sites, backup mysql db, backup wp files)
- Restore site



### Extra Features (explain feature/complexity tradeoffs at the end)

- Caching? CDN?
- create and store letsencrypt TLS cert for a domain
- use TLS cert (nginx)

- Create another plan type that has a LOCAL instance of MySQL running.
    - Management script changes needed?

- Force WordPress update on server? Maybe not...









# For End-Users

## Features

- Security & Performance: Each WordPress site is run on its own VM
- Each WordPress site has its own cache
- Safe, per-site SSH logins (for clients) possible



## Infrastructure

- *Google Cloud* -- lower cost and better features than Amazon AWS, while teaching you the same basic concepts.
- Isolated websites, each on their own VM.
- Shared MySQL DB (managed by Google) - better performance and lower total cost of ownership.



## HOWTO

    # Create a Python virtual environment for this project and install dependencies
    cd $THIS_DIRECTORY
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    cd fabfile


