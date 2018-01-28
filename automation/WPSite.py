class WPSite(object):
    """A WordPress Site"""
    def __init__(self, dbname, dbuser, dbpass, dbhost, domain, webhost, ip, cloud):
        super(WPSite, self).__init__()

        # Database Settings
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbhost = dbhost

        # Webserver Settings
        self.domain = domain
        self.webhost = webhost # a digitalocean ID
        self.ip = ip
        self.cloud = cloud # DO, GCP, AWS?

        # State
        self.active = False
