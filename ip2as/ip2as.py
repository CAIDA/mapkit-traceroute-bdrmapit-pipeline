#!/usr/bin/env python
from argparse import ArgumentParser, FileType
from typing import List, Tuple

from traceutils.as2org.as2org import AS2Org
from traceutils.bgp.bgp import BGP
from traceutils.file2.file2 import File2
from traceutils.ixps import AbstractPeeringDB, create_peeringdb
from traceutils.radix.ip2as import IP2AS


def valid(asn):
    return asn != 23456 and 0 < asn < 64496 or 131071 < asn < 400000

def create_table(prefixes: List[Tuple[str, str]], peeringdb: AbstractPeeringDB, rir: List[Tuple[str, str]], bgp: BGP, as2org: AS2Org):
    table = IP2AS()
    table.add_private()
    ixp_prefixes = [(prefix, asn) for prefix, asn in peeringdb.prefixes.items() if not table.search_best_prefix(prefix)]
    for prefix, ixp_id in ixp_prefixes:
        table.add_asn(prefix, asn=(-100 - ixp_id))
    prefixes = [(prefix, asn_s) for prefix, asn_s in prefixes if not table.search_best_prefix(prefix)]
    for prefix, asn_s in prefixes:
        asn = determine_bgp(asn_s, as2org, bgp)
        table.add_asn(prefix, asn=asn)
    if rir:
        rir = [(prefix, asn_s) for prefix, asn_s in rir if not table.search_best_prefix(prefix)]
        for prefix, asn_s in rir:
            asns = list(map(int, asn_s.split('_')))
            if len(asns) > 1:
                asn = max(asns, key=lambda x: (bgp.conesize[x]))
            else:
                asn = asns[0]
            table.add_asn(prefix, asn=asn)
    return table

def determine_bgp(asn_s, as2org: AS2Org, bgp: BGP):
    asns = []
    for asn in asn_s.split('_'):
        if asn[0] == '{':
            for asn in asn[1:-1].split(','):
                asn = int(asn)
                asns.append(asn)
        else:
            asns.append(int(asn))
    if len(asns) == 1:
        return asns[0]
    orgs = {as2org[asn] for asn in asns}
    if len(orgs) == 1:
        return asns[0]
    for asn in asns:
        if all(asn in bgp.cone[other] for other in asns if other != asn):
            return asn
    # mins = max_num(asns, key=lambda x: -bgp.conesize[x])
    # if mins:
    #     return mins[0]
    return asns[0]

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
                if prefixlen <= 8:
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
    parser.add_argument('-P', '--peeringdb', required=True, help='PeeringDB json file or sqlite database.')
    parser.add_argument('-r', '--rir', required=False, help='RIR prefix-to-AS file, optional but recommended to fill in missing prefixes.')
    parser.add_argument('-R', '--rels', required=True, help='AS relationship file in the standard CAIDA format.')
    parser.add_argument('-c', '--cone', required=True, help='AS customer cone file in the standard CAIDA format.')
    parser.add_argument('-o', '--output', type=FileType('w'), default='-', help='Output file.')
    parser.add_argument('-a', '--as2org', required=True, help='AS-to-Org mappings in the standard CAIDA format.')
    args = parser.parse_args()

    ixp = create_peeringdb(args.peeringdb)
    bgp = BGP(args.rels, args.cone)
    as2org = AS2Org(args.as2org)
    prefixes = read_prefixes(args.prefixes)
    rir = read_prefixes(args.rir) if args.rir else None
    table = create_table(prefixes, ixp, rir, bgp, as2org)
    for node in table.nodes():
        args.output.write('{} {}\n'.format(node.network, node.asn))

if __name__ == '__main__':
    main()
