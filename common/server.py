class Server:

    def __init__(self, hostname):
        self.hostname = hostname

    def is_available(self, discovery_module):
        return discovery_module.is_host_available(self.hostname)
    
    def execute_command_and_get_output(self, proxy, user, command:str):
        if user.can_execute_on_server(self):
            return proxy.execute_command_and_get_output(user, self.hostname, command)

    def execute_script_and_get_output(self, proxy, user, script_path:str):
        if user.can_execute_on_server(self):
            return proxy.execute_script_and_get_output(user, self.hostname, script_path)
