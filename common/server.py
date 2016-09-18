class Server:

    def __init__(self, hostname):
        self.hostname = hostname
    
    def execute_command_and_get_output(self, proxy, user, command:str):
        return proxy.execute_command_and_get_output(user, self.hostname, command)

    def execute_script_and_get_output(self, proxy, user, script_path:str):
        return proxy.execute_script_and_get_output(user, self.hostname, script_path)