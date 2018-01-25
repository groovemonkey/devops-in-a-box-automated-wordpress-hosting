# Automated WordPress (or other dynamic website) hosting


## Dave's TODO

1. finish 'master instance' setup
1. create disk image
1. create a (.gitignore'd) config file for mysql login info, admin SSH keys (?), other sensitive data
1. flesh out admin tasks in fabfile
    - create_instance function (import/transplant all code from helpers.py)
    - wp-config.php templating function
    - new instance setup script -- install and configure a single WP site -- scripts/set-up-wp-site.sh (pass it in as a startup script with metadata? Or trigger configuration via fabric? Not sure yet.)

1. create mysql master (Google-managed)



## Filming plan:

- Separate theory/skill and 'practical tutorial' videos, to make re-filming sections easier as API changes happen? Separate 'teaching' and 'showing.'




## AUTOMATION TODO


### Low-level Automation

These automation tasks map directly to implementation-specific concepts. They form the foundation for higher-level automation functions.

- Spin up compute instance from base image
- Create a site DB user on the cluster
- Create a wp-config.php file from site metadata (hostname, mysql auth/endpoint info, etc.)
- list active sites
- backup mysql db
- backup wp files


### High-level automation

These automation functions map directly to the BUSINESS GOALS that our application carries out. They are composed of low-level, implementation-hiding functions. These high-level automation functions are called directly by our management scripts and fab tasks.

- Create new site (spin up base image, create site DB user, create a wp-config.php file)
- Enable/Disable site (nginx stop)
- Update mysql endpoint for a site
- Back up site (list active sites, backup mysql db, backup wp files)
- Restore site



### Extra Features (explain feature/complexity tradeoffs at the end)

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

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt


