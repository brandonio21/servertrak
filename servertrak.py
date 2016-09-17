#!/usr/bin/env python3
import argparse
import fileinput
import sys
import contextlib
import yaml
from proxies.ssh import SSHProxy
from utils import flexio
from common.server import Server
from common.user import User


def main():
    argument_parser = argparse.ArgumentParser(
        description="Replicate commands across servers")

    argument_parser.add_argument("commands")

    # Config files
    argument_parser.add_argument('--config', type=str, nargs=1, default='servers.yaml')

    # Output
    argument_parser.add_argument('-output', type=str, nargs=1, default='-')

    # Proxy types
    proxy_parser = argument_parser.add_mutually_exclusive_group()
    proxy_parser.add_argument('--ssh', action='store_true', default=True)


    args = argument_parser.parse_args()

    if args.ssh:
        proxy = SSHProxy()

    servers, users = parse_config(args.config)
    execute_command(proxy, servers, users, construct_input(), args.output)

def construct_input() -> str:
    full_input = ""
    for line in fileinput.input():
        full_input += line

    return full_input

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

def execute_command(proxy, servers: list, users: list, command:str, output:str):
    with flexio.open_io(output) as output_stream:
        for server in servers:
            for user in users:
                output_stream.write(server.get_command_output(proxy, command))

if __name__ == "__main__":
    main()