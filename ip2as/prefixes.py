#!/usr/bin/env python
import sys
from argparse import ArgumentParser, FileType
from collections import Counter, defaultdict
from multiprocessing.pool import Pool

from traceutils.bgpreader.reader import read
from traceutils.progress.bar import Progress


def extract_prefixes(filenames, processes):
    counter = Counter()
    pb = Progress(len(filenames), 'Test', callback=lambda: 'Prefixes {:,d}'.format(len(counter)))
    with Pool(processes) as pool:
        for newcounter in pb.iterator(pool.imap_unordered(read, filenames)):
            counter.update(newcounter)
    return counter


def reduce(counter):
    nets = defaultdict(list)
    for (prefix, asn), num in counter.most_common():
        nets[prefix].append(asn)
    return nets


def write(file, nets):
    for prefix, asns in nets.items():
        if not prefix.endswith(b'/0'):
            file.write(prefix + b'\t' + b'_'.join(asns) + b'\n')


def main():
    parser = ArgumentParser()
    parser.add_argument('-o', '--output', type=FileType('wb'), default=sys.stdout, help='Output filename')
    parser.add_argument('-p', '--processes', type=int, default=1, help='Processes to use when parsing the RIB files')
    parser.add_argument('-r', '--ribs', required=True, type=FileType('r'), help='RIB filenames, newline separated')
    args = parser.parse_args()

    files = []
    for line in args.ribs:
        line = line.strip()
        if line and line[0] != '#':
            files.append(line)
    counter = extract_prefixes(files, args.processes)
    nets = reduce(counter)
    write(args.output, nets)


if __name__ == '__main__':
    main()
