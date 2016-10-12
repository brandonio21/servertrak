


class ServerTraker(object):
    
    def __init__(self, 
                 host_discovery_modules,
                 output_builder,
                 proxy,
                 require_all_discovery_modules=False):
        self.host_discovery_modules = host_discovery_modules
        self.output_builder = output_builder
        self.proxy = proxy
        self.require_all_discovery_modules = require_all_discovery_modules
        
    def get_available_servers(self, servers):
        available_servers = []
        for server in servers:
            if self.require_all_discovery_modules:
                requirement_func = all
            else:
                requirement_func = any
                
            if requirement_func([server.is_available(module) for module
                                 in self.host_discovery_modules]):
                available_servers.append(server)
                
        return available_servers
        
        
    def execute_command(self, servers, users, command):
        self.output_builder.clear_output()
        for server in servers:
            for user in users:
                try:
                    server_output = server.execute_command_and_get_output(
                        self.proxy, user, command
                    )
                    self.output_builder.add_output(user, server, server_output)
                except Exception as e:
                    self.output_builder.add_err(user, server, str(e))
                    
        return self.output_builder.build_output()