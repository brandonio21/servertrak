#!/usr/bin/env python3
import argparse
import sys
import contextlib
import yaml
from exrex import exrex
from proxies.ssh import SSHProxy
from utils import flexio
from common.server import Server
from common.user import User
from common.output.jsonoutput import JSONOutput
from common.output.text import TextOutput
from host_discovery.ping import PingHostDiscoveryModule

def main():
    argument_parser = argparse.ArgumentParser(
        description="Replicate commands across servers")

    argument_parser.add_argument("command")

    # Config files
    argument_parser.add_argument('--config', type=str, nargs=1, default='servers.yaml')

    # Output
    argument_parser.add_argument('-output', type=str, default='-')
    argument_parser.add_argument('--output-type', type=str, default='json', dest='outputtype')

    # Script
    argument_parser.add_argument('--script', action='store_true')

    # Proxy types
    proxy_parser = argument_parser.add_mutually_exclusive_group()
    proxy_parser.add_argument('--ssh', action='store_true', default=True)

    # Host Discovery
    argument_parser.add_argument('--discovery', default='ping')

    args = argument_parser.parse_args()

    if args.ssh:
        proxy = SSHProxy()
    else:
        raise ValueError('Invalid proxy type')

    if args.outputtype == 'json':
        output = JSONOutput()
    elif args.outputtype == 'text':
        output = TextOutput()
    else:
        raise ValueError('Invalid value for outputtype {}'.format(args.outputtype))

    if args.discovery == 'ping':
        host_discovery_module = PingHostDiscoveryModule()
    else:
        raise ValueError('Invalid value for discovery {}'.format(args.discovery))

    servers, users = parse_config(args.config)
    available_servers = get_available_servers(servers, host_discovery_module)
    execute_command_and_write(proxy, available_servers, users, args.command, args.script, args.output, output)

def parse_config(config_path):
    with open(config_path) as config_file:
        config = yaml.load(config_file.read())

    server_list = []
    user_list = []
    if config:
        hostname_set = set()
        if 'servers' in config:
            for hostname in config['servers']:
                hostname_set.add(hostname)

        if 'discover_servers' in config:
            for hostname_pattern in config['discover_servers']:
                for hostname in generate_servers_from_regex(hostname_pattern):
                    hostname_set.add(hostname)

        for hostname in hostname_set:
            server_list.append(Server(hostname))

        for user in config['users']:
            user_list.append(User(user['username'], user['servers']))

    return (server_list, user_list)

def generate_servers_from_regex(server_regex):
    for server in exrex.generate(server_regex):
        yield server

def get_available_servers(servers, host_discovery_module):
    available_servers = []
    for server in servers:
        if server.is_available(host_discovery_module):
            available_servers.append(server)

    return available_servers

def execute_command(proxy, servers, users, command, is_script, output_builder):
    for server in servers:
        for user in users:
            try:
                if is_script:
                    server_output = server.execute_script_and_get_output(proxy, user, command)
                else:
                    server_output = server.execute_command_and_get_output(proxy, user, command)

                output_builder.add_output(user, server, server_output)
            except Exception as e:
                output_builder.add_err(user, server, str(e))

    return output_builder.build_output()


def execute_command_and_write(proxy, servers, users, command, is_script, output, output_builder):
    results = execute_command(proxy, servers, users, command, is_script, output_builder)

    with flexio.open_io(output) as output_stream:
        output_stream.write(results)

if __name__ == "__main__":
    main()
