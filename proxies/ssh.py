import subprocess

class SSHProxy:
    def execute_command_and_get_output(self, user, hostname, command: str):
        return subprocess.check_output(['ssh', '{}@{}'.format(user.username, hostname), command])

    def execute_script_and_get_output(self, user, hostname, script_path: str):
        return "script-output"
