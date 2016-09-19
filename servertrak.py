#!/usr/bin/env python3
import argparse
import sys
import contextlib
import yaml
from proxies.ssh import SSHProxy
from utils import flexio
from common.server import Server
from common.user import User
from common.output.json import JSONOutput

def main():
    argument_parser = argparse.ArgumentParser(
        description="Replicate commands across servers")

    argument_parser.add_argument("command")

    # Config files
    argument_parser.add_argument('--config', type=str, nargs=1, default='servers.yaml')

    # Output
    argument_parser.add_argument('-output', type=str, default='-')
    argument_parser.add_argument('--output-type', type=str, nargs=1, default='json', dest='outputtype')

    # Script
    argument_parser.add_argument('--script', action='store_true')

    # Proxy types
    proxy_parser = argument_parser.add_mutually_exclusive_group()
    proxy_parser.add_argument('--ssh', action='store_true', default=True)

    args = argument_parser.parse_args()

    if args.ssh:
        proxy = SSHProxy()

    if args.outputtype == 'json':
        output = JSONOutput()

    servers, users = parse_config(args.config)
    execute_command(proxy, servers, users, args.command, args.script, args.output, output)

def parse_config(config_path):
    with open(config_path) as config_file:
        config = yaml.load(config_file.read())

    server_list = []
    user_list = []
    if config:
        for server in config['servers']:
            server_list.append(Server(server))

        for user in config['users']:
            user_list.append(User(user['username'], user['servers']))

    return (server_list, user_list)

def execute_command(proxy, servers: list, users: list, command:str, is_script:bool, output:str, output_builder):
    for server in servers:
        for user in users:
            if is_script:
                server_output = server.execute_script_and_get_output(proxy, user, command)
            else:
                server_output = server.execute_command_and_get_output(proxy, user, command)

            output_builder.add_output(user, server, server_output)

    with flexio.open_io(output) as output_stream:
        output_stream.write(output_builder.build_output())

if __name__ == "__main__":
    main()
