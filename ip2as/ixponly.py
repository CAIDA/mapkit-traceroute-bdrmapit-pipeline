#!/usr/bin/env python
from argparse import ArgumentParser, FileType

from traceutils.ixps import create_peeringdb, AbstractPeeringDB
from traceutils.radix.ip2as import IP2AS

def create_table(peeringdb: AbstractPeeringDB):
    table = IP2AS()
    table.add_private()
    ixp_prefixes = [(prefix, asn) for prefix, asn in peeringdb.prefixes.items() if not table.search_best_prefix(prefix)]
    for prefix, ixp_id in ixp_prefixes:
        table.add_asn(prefix, asn=(-100 - ixp_id))
    return table

def main():
    parser = ArgumentParser()
    parser.add_argument('-P', '--peeringdb', required=True, help='PeeringDB json file or sqlite database.')
    parser.add_argument('-o', '--output', type=FileType('w'), default='-', help='Output file.')
    args = parser.parse_args()

    ixp = create_peeringdb(args.peeringdb)
    table = create_table(ixp)
    for node in table.nodes():
        args.output.write('{} {}\n'.format(node.network, node.asn))

if __name__ == '__main__':
    main()
