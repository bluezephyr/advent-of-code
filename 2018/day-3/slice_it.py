#!/usr/bin/env python3
import argparse
import time


class Claim():
    def __init__(self):
        self.id = 0
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def parse(self, item):
        r = item.split(' ')
        self.id = int(r[0][1:])
        self.x = int(r[2].split(',')[0])
        self.y = int(r[2].split(',')[1][:-1])
        self.w = int(r[3].split('x')[0])
        self.h = int(r[3].split('x')[1])

        def ajkf(self):
            pass



def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 3')
    parser.add_argument('input', help='File name for the input to parse')
    return parser.parse_args()


def parse_file(filename):
    """
    Parse the input file, line by line, and return a list of all the items.
    """
    item_list = []
    with open(args.input) as f:
        for item in f.readlines():
            item_list.append(item[:-1])
    return item_list


def part_I(input):
    print('Part I')
    all_claims = set()
    overlaps = set()

    for item in input:
        claim = Claim()
        claim.parse(item)

        for y in range(claim.h):
            for x in range(claim.w):
                if ((claim.x+x, claim.y+y)) in all_claims:
                    overlaps.add((claim.x+x, claim.y+y))
                all_claims.add((claim.x+x, claim.y+y))

    print('Number of overlaps: {}'.format(len(overlaps)))
    return overlaps


def part_II(input, overlaps):
    print('Part II')

    for item in input:
        claim = Claim()
        claim.parse(item)
        overlap = False

        for y in range(claim.h):
            for x in range(claim.w):
                if ((claim.x+x, claim.y+y)) in overlaps:
                    overlap = True

        if not overlap:
            print('Claim #{} does not overlap any other claims'.format(claim.id))


if __name__ == '__main__':
    start_time = time.time()
    args = parse_arguments()

    id_list = parse_file(args.input)

    overlaps_set = part_I(id_list)
    part_II(id_list, overlaps_set)

    print('Finished in {} seconds'.format(time.process_time()))

