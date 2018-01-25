#!/usr/bin/env bash

THIS SHOULD BE A FAB TASK OR ANSIBLE PLAYBOOK

############
# Identical to https://github.com/groovemonkey/hands_on_linux-self_hosted_wordpress_for_linux_beginners/blob/master/7-set-up-wordpress-site.md
############
useradd yourusername

# Create the php-fpm logfile
mkdir -p /home/yourusername/logs
touch /home/yourusername/logs/phpfpm_error.log









# nano /etc/nginx/conf.d/yoursitename.conf

server {
    listen       80;
    server_name  www.{{ domain_name }};

    client_max_body_size 20m;

    index index.php index.html index.htm;
    root   /home/yourusername/public_html;

    location / {
        try_files $uri $uri/ /index.php?q=$uri&$args;
    }

    # pass the PHP scripts to FastCGI server
    location ~ \.php$ {
            # Basic
            try_files $uri =404;
            fastcgi_index index.php;

            # Create a no cache flag
            set $no_cache "";

            # Don't ever cache POSTs
            if ($request_method = POST) {
              set $no_cache 1;
            }

            # Admin stuff should not be cached
            if ($request_uri ~* "/(wp-admin/|wp-login.php)") {
              set $no_cache 1;
            }

            # WooCommerce stuff should not be cached
            if ($request_uri ~* "/store.*|/cart.*|/my-account.*|/checkout.*|/addons.*") {
              set $no_cache 1;
            }

            # If we are the admin, make sure nothing
            # gets cached, so no weird stuff will happen
            if ($http_cookie ~* "wordpress_logged_in_") {
              set $no_cache 1;
            }

            # Cache and cache bypass handling
            fastcgi_no_cache $no_cache;
            fastcgi_cache_bypass $no_cache;
            fastcgi_cache microcache;
            fastcgi_cache_key $scheme$request_method$server_name$request_uri$args;
            fastcgi_cache_valid 200 60m;
            fastcgi_cache_valid 404 10m;
            fastcgi_cache_use_stale updating;


            # General FastCGI handling
            fastcgi_pass unix:/var/run/php/yoursitename.sock;
            fastcgi_pass_header Set-Cookie;
            fastcgi_pass_header Cookie;
            fastcgi_ignore_headers Cache-Control Expires Set-Cookie;
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            fastcgi_param SCRIPT_FILENAME $request_filename;
            fastcgi_intercept_errors on;
            include fastcgi_params;         
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|woff|ttf|svg|otf)$ {
            expires 30d;
            add_header Pragma public;
            add_header Cache-Control "public";
            access_log off;
    }

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}

server {
    listen       80;
    server_name  {{ domain_name }};
    rewrite ^/(.*)$ http://www.{{ domain_name }}/$1 permanent;
}











# Create php-fpm vhost pool config file
[yoursitename]
listen = /var/run/php/yoursitename.sock
listen.owner = yourusername
listen.group = www-data
listen.mode = 0660
user = yourusername
group = www-data
pm = dynamic
pm.max_children = 75
pm.start_servers = 8
pm.min_spare_servers = 5
pm.max_spare_servers = 20
pm.max_requests = 500

php_admin_value[upload_max_filesize] = 25M
php_admin_value[error_log] = /home/yourusername/logs/phpfpm_error.log
php_admin_value[open_basedir] = /home/yourusername:/tmp














# Create a DB user
# Create password
echo -n @ && cat /dev/urandom | env LC_CTYPE=C tr -dc [:alnum:] | head -c 15 && echo

mysql -u root -p

# Log into mysql
CREATE DATABASE yoursite;
CREATE USER yoursite@localhost IDENTIFIED BY 'chooseapassword';
GRANT ALL PRIVILEGES ON yoursite.* TO yoursite@localhost IDENTIFIED BY 'chooseapassword';
FLUSH PRIVILEGES;






# Install WordPress

su - yourusername

# Download and cleanup
wget https://wordpress.org/latest.tar.gz
tar zxf latest.tar.gz
rm latest.tar.gz

mv wordpress public_html




# Exit the unprivileged user's shell and become root again

cd /home/yourusername/public_html
chown -R yourusername:www-data .
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;



systemctl restart php7.0-fpm nginx




ONCE YOU HAVE RUN THE WORDPRESS INSTALLER...

You'll be able to run the installer by navigating to your server IP address in a browser. Once you've done that...
Secure the wp-config.php file so other users can’t read DB credentials

chmod 640 /home/yourusername/public_html/wp-config.php
















