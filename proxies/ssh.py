import subprocess

class SSHProxy:
    def execute_command_and_get_output(self, user, hostname, command: str):
        return subprocess.check_output(['ssh', '{}@{}'.format(user.username, hostname), command]).decode('utf-8')

    def execute_script_and_get_output(self, user, hostname, script_path: str):
        with open(script_path, 'r') as script:
            return subprocess.check_output(['ssh', '{}@{}'.format(user.username, hostname), 'bash', '-s'], stdin=script).decode('utf-8')
