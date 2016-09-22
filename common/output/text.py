class TextOutput:
    def __init__(self):
        self.output = []

    def add_output(self, user, server, output: str):
        output_str = '{} ({}): {}'.format(server.hostname, user.username, 
                                          output)
        self.output.append(output_str)

    def build_output(self) -> str:
        return '\n'.join(self.output) 

