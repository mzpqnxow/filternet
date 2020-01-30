#!/usr/bin/env python3
"""
Given a list of IPv4 addresses or networks in CIDR notation,
filter based on a blacklist of IPv4 addresses or networks
"""
from ipaddress import ip_network
from argparse import ArgumentParser
from sys import stderr, stdin, argv


def error(message):
    """Write to stderr with a newline"""
    stderr.write(message + '\n')


def load_network_lines(infile):
    """Load a line-based file into a list of unique ip_network objects

    Example input:
        ...
        1.2.3.4
        2.2.3.4/32
        3.2.3.0/24
        4.2.3.0/24  # Comment
        ...
    """
    network_lines = list()

    try:
        infd = stdin if infile is None else open(infile, 'r')
    except OSError as err:
        error(repr(err))
        exit(1)

    lines = {line.strip() for line in infd.readlines()}
    for line in lines:
        if not line:
            continue
        if '#' in line:  # Allow comments
            line = line.split('#')[0].strip()

        try:
            if line.endswith('/32'):
                # Python ip_network chokes on a /32 network
                # Yet it accepts 4 octets without a mask...
                line = line[0:-3]
            net = ip_network(line, strict=False)
            network_lines.append(net)
        except ValueError as err:
            error('Skipping bad line: {}'.format(line))
            error(repr(err))
    return network_lines


def cli(appname):
    """Simple CLI argument parsing"""
    argparser = ArgumentParser(prog=appname)
    argparser.add_argument(
        '-b',
        '--blacklist-file',
        dest='blacklist_file',
        required=True,
        help='Path to file containing blacklisted IPv4 address / networks input list',
        metavar='blacklist.lst')
    argparser.add_argument(
        '-i',
        '--input-file',
        required=False,
        default=None,
        dest='input_file',
        metavar='networks.lst',
        help='Path to unfiltered IPv4 address / networks input list, stdin by default')
    argparser.add_argument(
        '-o',
        '--output-base',
        dest='output_base',
        default='output-nets',
        help='Basename for output files, .rejected.lst and .accepted.lst will be created',
        metavar='output-nets')
    args = argparser.parse_args()
    return args


def main():
    """There must be a command-line tool to do this ..."""
    args = cli(argv[0])
    rejected_nets = list()
    accepted_nets = list()
    input_lines = load_network_lines(args.input_file)
    blacklist_nets = load_network_lines(args.blacklist_file)
    for checknet in input_lines:
        for blacknet in blacklist_nets:
            if checknet[0] in blacknet:
                error('Blacklisting {} (in {})'.format(
                    checknet.exploded, blacknet.exploded))
                rejected_nets.append(checknet.exploded)
                break
        else:
            error('Keeping {}'.format(checknet.exploded))
            accepted_nets.append(checknet.exploded)
            print(checknet.exploded)

    output_map = {
        '-accepted.lst': accepted_nets,
        '-rejected.lst': rejected_nets,
    }

    for suffix, obj in output_map.items():
        with open('{}{}'.format(args.output_base, suffix), 'w') as outfd:
            outfd.write('\n'.join(obj))
            outfd.write('\n')


if __name__ == '__main__':
    main()
