import json


class JSONOutput:
    def __init__(self):
        self.output = []

    def clear_output(self):
        self.output = []

    def add_output(self, user, server, output, success=1):
        self.output.append({
            'server': server.hostname,
            'user': user.username,
            'success': str(success),
            'output': output})

    def add_err(self, user, server, err):
        self.add_output(user, server, err, success=0)

    def build_output(self):
        return json.dumps(self.output, indent=4, separators=(',', ':'))
