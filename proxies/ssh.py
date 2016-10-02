from subprocess import Popen, PIPE

class SSHProxy:
    def execute_command_and_get_output(self, user, hostname, command: str):
        p = Popen(['ssh', '{}@{}'.format(user.username, hostname), command],
                  stdout=PIPE, stderr=PIPE)
        stdoutdata, stderrdata = p.communicate()

        if p.returncode == 0:
            return stdoutdata.decode('utf-8')
        else:
            raise Exception(stderrdata.decode('utf-8'))

    def execute_script_and_get_output(self, user, hostname, script_path: str):
        with open(script_path, 'r') as script:
            p = Popen(['ssh', '{}@{}'.format(user.username, hostname), 'bash',
                      '-s'], stdout=PIPE, stderr=PIPE)
            
            stdoutdata, stderrdata = p.communicate(input=script)

            if p.returncode == 0:
                return stdoutdata.decode('utf-8')
            else:
                raise Exception(stderrdata.decode('utf-8'))

