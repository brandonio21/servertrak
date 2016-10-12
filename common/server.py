class Server:

    def __init__(self, hostname):
        self.hostname = hostname

    def is_available(self, discovery_module):
        return discovery_module.is_host_available(self.hostname)
    
    def execute_command_and_get_output(self, proxy, user, command):
        if user.can_execute_on_server(self):
            return proxy.execute_command_and_get_output(user, self.hostname, command)