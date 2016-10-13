from subprocess import Popen, PIPE


class PingHostDiscoveryModule:

    def is_host_available(self, hostname):
        p = Popen(['ping', hostname, '-c', '1'], stdout=PIPE, stderr=PIPE)
        p.wait()

        return p.returncode == 0
