import fnmatch

class User:

    def __init__(self, username, servers):
        self.username = username
        self.servers = servers

    def can_execute_on_server(self, server):
        for allowed_server in self.servers:
            if fnmatch.fnmatch(server.hostname, allowed_server):
                return True

        return False
