class Server:

    def __init__(self, hostname):
        self.hostname = hostname

    def get_command_output(self, proxy, command: str):
        """ Sends a command to the server and returns the output 

        command: list<str> the command to execute, where the first element
                 is usually the commandname and the rest are args
        """
        return proxy.get_command_output(self.hostname, command)