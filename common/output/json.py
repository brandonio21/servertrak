import json

class JSONOutput:
    def __init__(self):
        self.output = []

    def add_output(self, user, server, output: str):
        self.output.append({
            'server' : server.hostname,
            'user'   : user.username,
            'output' : output})

    def build_output(self) -> str:
        return json.dumps(self.output, indent=4, separators=(',', ':'))
