#!/usr/bin/env python3
import yaml
import click
import exrex
from proxies import ALL_PROXIES
from format import ALL_OUTPUT
from host_discovery import ALL_DISCOVERY_MODULES
from servertraker import ServerTraker
from common.server import Server
from common.user import User


@click.command()
@click.argument('command', type=click.File('rb'), default='-')
@click.option('--output', type=click.File('wb'), default='-')
@click.option('--config', type=click.Path(exists=True), default='servers.yaml')
@click.option('--proxy', default='ssh')
@click.option('--discovery', default='ping')
@click.option('--format', default='text')
def main(command, output, config, proxy, discovery, format):
    if proxy in ALL_PROXIES:
        proxy = ALL_PROXIES[proxy]()
    else:
        raise ValueError('Invalid proxy type')

    if discovery in ALL_DISCOVERY_MODULES:
        discovery_module = ALL_DISCOVERY_MODULES[discovery]()
    else:
        raise ValueError('Invalid discovery module')

    if format in ALL_OUTPUT:
        format = ALL_OUTPUT[format]()
    else:
        raise ValueError('Invalid output method')

    servertraker = ServerTraker(
        [discovery_module], format, proxy
    )

    servers, users = parse_config(config)
    available_servers = servertraker.get_available_servers(servers)
    results = servertraker.execute_command(
        available_servers, users, command.read().decode('utf-8')
    )

    output.write(bytes(results, 'utf-8'))


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

if __name__ == "__main__":
    main()
