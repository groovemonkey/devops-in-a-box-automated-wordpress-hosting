class WPSite(object):
    """
    A WordPress Site. This class may be unnecessary -- it's really just a dict.
    Waiting to see if there are methods that would make sense for this.
    For that to be realistic, we'd need to make this persistent via sqlite or pickle.
    """
    def __init__(self, dbhost, dbname, dbuser, dbpass, domain, cloud="DO"):
        super(WPSite, self).__init__()

        # Database Settings
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbhost = dbhost

        # Webserver Settings
        self.domain = domain
        self.hostid = None # a digitalocean ID
        self.ip = None
        self.cloud = cloud # DO, GCP, AWS?

        # State
        self.active = False
