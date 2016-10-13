from subprocess import Popen, PIPE


class SSHProxy:
    def execute_command_and_get_output(self, user, hostname, command):
        p = Popen(['ssh', '{}@{}'.format(user.username, hostname), command],
                  stdout=PIPE, stderr=PIPE)
        stdoutdata, stderrdata = p.communicate()

        if p.returncode == 0:
            return stdoutdata.decode('utf-8')
        else:
            raise Exception(stderrdata.decode('utf-8'))
