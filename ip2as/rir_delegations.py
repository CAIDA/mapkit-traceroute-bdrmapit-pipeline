#!/usr/bin/env python
import math
import socket
from argparse import ArgumentParser
from collections import defaultdict

from traceutils.file2.file2 import File2
from traceutils.progress.bar import Progress


def rirparse(filename):
    oasns = defaultdict(set)
    prefixes = []
    with File2(filename) as f:
        for line in f:
            splits = line.strip().split('|')
            if len(splits) >= 8:
                _, _, version, data, num, date, allocation, org = splits
                if version == 'ipv4' or version == 'ipv6':
                    # if data == '2001:506:100::':
                    #     print(data, num, org)
                    prefixes.append((data, int(num), org))
                elif version == 'asn':
                    oasns[org].add(data)
    for net, num, org in prefixes:
        asns = oasns[org]
        if asns:
            for network, prefixlen in prefixes_iter(net, num):
                yield network, prefixlen, asns


def prefixlen_iter(num):
    while True:
        total_bits = math.log2(num)
        bits = int(total_bits)
        yield bits
        if total_bits == bits:
            break
        else:
            num -= 2**bits


def prefixes_iter(address, num):
    if ':' not in address:
        fam = socket.AF_INET
        b = socket.inet_pton(fam, address)
        bitlen = len(b) * 8
        ipnum = int.from_bytes(b, 'big')
        for bits in prefixlen_iter(num):
            network = socket.inet_ntop(fam, ipnum.to_bytes(len(b), 'big'))
            prefixlen = bitlen - bits
            if prefixlen > 8:
                yield network, prefixlen
            ipnum += 2 ** bits
    else:
        fam = socket.AF_INET6
        yield address, num


def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--files')
    group.add_argument('-F', '--filelist', nargs='+')
    parser.add_argument('-r', '--rels')
    parser.add_argument('-c', '--cone')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    if args.files:
        with File2(args.files) as f:
            files = [line.strip() for line in f]
    else:
        files = args.filelist
    prefixes = defaultdict(set)
    pb = Progress(len(files), 'Parsing RIR delegations', callback=lambda: 'Prefixes {:,d}'.format(len(prefixes)))
    for filename in pb.iterator(files):
        for network, prefixlen, asns in rirparse(filename):
            prefixes[network, prefixlen].update(asns)
    with open(args.output, 'w') as f:
        f.writelines('{}/{}\t{}\n'.format(network, prefixlen, '_'.join(asns)) for (network, prefixlen), asns in prefixes.items())


if __name__ == '__main__':
    main()
