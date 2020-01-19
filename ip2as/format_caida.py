#!/usr/bin/env python
from argparse import ArgumentParser, FileType
from sys import stdout

parser = ArgumentParser()
parser.add_argument('-i', '--input', required=True, type=FileType('r'))
parser.add_argument('-o', '--output', type=FileType('w'), default=stdout)
parser.add_argument('-p', '--private', action='store_true')
parser.add_argument('-x', '--ixp', action='store_true')
parser.add_argument('-4', '--ipv6', action='store_false')
parser.add_argument('-6', '--ipv4', action='store_false')
args = parser.parse_args()
for line in args.input:
    prefix, asn = line.split()
    if args.ipv4 and ':' in prefix:
        continue
    if args.ipv6 and ':' not in prefix:
        continue
    asn = int(asn)
    if not args.private and -100 < asn < 0:
        continue
    if args.ixp:
        if asn > -100:
            continue
        args.output.write('{}\n'.format(prefix))
    else:
        if asn <= -100:
            continue
        net, _, plen = prefix.partition('/')
        args.output.write('{}\t{}\t{}\n'.format(net, plen, asn))
