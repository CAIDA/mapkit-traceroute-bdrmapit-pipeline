#!/usr/bin/env python
from argparse import ArgumentParser, FileType
from typing import List, Tuple

from traceutils.file2 import File2
from traceutils.ixps.ixps import PeeringDB
from traceutils.radix.ip2ases import IP2ASes


def valid(asn):
    return asn != 23456 and 0 < asn < 64496 or 131071 < asn < 400000


def create_table(prefixes: List[Tuple[str, str]], peeringdb: PeeringDB, rir: List[Tuple[str, str]]):
    table = IP2ASes()
    table.add_private()
    ixp_prefixes = [(prefix, asn) for prefix, asn in peeringdb.prefixes.items() if not table.search_best_prefix(prefix)]
    for prefix, ixp_id in ixp_prefixes:
        table.add_asns(prefix, asns=[(-100 - ixp_id)])
    prefixes = [(prefix, asn_s) for prefix, asn_s in prefixes if not table.search_best_prefix(prefix)]
    for prefix, asn_s in prefixes:
        asns = determine_bgp(asn_s)
        table.add_asns(prefix, asns=asns)
    if rir:
        rir = [(prefix, asn_s) for prefix, asn_s in rir if not table.search_best_prefix(prefix)]
        for prefix, asn_s in rir:
            asns = list(map(int, asn_s.split('_')))
            table.add_asns(prefix, asns=asns)
    return table


def determine_bgp(asn_s):
    asns = []
    for asn in asn_s.split('_'):
        if asn[0] == '{':
            for asn in asn[1:-1].split(','):
                asn = int(asn)
                asns.append(asn)
        else:
            asns.append(int(asn))
    return asns


def read_prefixes(filename: str):
    prefixes = []
    try:
        with File2(filename) as f:
            for line in f:
                if line[0] == '#':
                    continue
                prefix, asn_s = line.split()
                prefixes.append((prefix, asn_s))
    except ValueError:
        with File2(filename, 'rt') as f:
            for line in f:
                if line[0] == '#':
                    continue
                addr, prefixlen, asn_s = line.split()
                asns = []
                for asn in asn_s.split('_'):
                    if asn.startswith('{'):
                        asn = asn[1:-1]
                    try:
                        asn = int(asn)
                        if valid(asn):
                            asns.append(asn)
                    except ValueError:
                        for a in asn[1:-1].split(','):
                            a = int(a)
                            if valid(a):
                                asns.append(a)
                if not asns:
                    continue
                asn_s = '_'.join(str(asn) for asn in asns)
                prefixlen = int(prefixlen)
                if prefixlen < 8:
                    continue
                if ':' in addr:
                    if prefixlen > 48:
                        continue
                else:
                    if prefixlen > 24:
                        continue
                prefix = '{}/{}'.format(addr, prefixlen)
                prefixes.append((prefix, asn_s))
    return prefixes


def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--prefixes', required=True, help='RIB prefix-to-AS file in the standard CAIDA format.')
    parser.add_argument('-P', '--peeringdb', required=True, help='PeeringDB json file.')
    parser.add_argument('-r', '--rir', required=False, help='RIR prefix-to-AS file, optional but recommended to fill in missing prefixes.')
    parser.add_argument('-o', '--output', type=FileType('w'), default='-', help='Output file.')
    args = parser.parse_args()

    ixp = PeeringDB(args.peeringdb)
    prefixes = read_prefixes(args.prefixes)
    rir = read_prefixes(args.rir) if args.rir else None
    table = create_table(prefixes, ixp, rir)
    for node in table.nodes():
        args.output.write('{} {}\n'.format(node.network, ','.join(str(asns) for asns in node.asns)))


if __name__ == '__main__':
    main()
