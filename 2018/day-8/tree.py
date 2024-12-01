#!/usr/bin/env python3
import argparse
import time


class Node():
    def __init__(self):
        self.children = []
        self.metadata = []

    def add_node(self, child):
        self.children.append(child)

    def add_meta(self, data):
        self.metadata.append(data)

    def calculate_meta(self):
        s = 0
        for item in self.children:
            s += item.calculate_meta()
        s += sum(self.metadata)
        return s

    def calculate_value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            s = 0
            for index in self.metadata:
                # Note index starts at 1
                if index <= len(self.children):
                    s += self.children[index-1].calculate_value()
            return s


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 8')
    parser.add_argument('input', help='File name for the input to parse')
    return parser.parse_args()


def parse_file(filename):
    """
    Parse the input file, line by line, and return a list of all the items.
    """
    with open(args.input) as f:
        for item in f.readlines():
            return item


def parse(input):
    node = Node()
    n_children = input.pop(0)
    n_meta = input.pop(0)
    for _ in range(n_children):
        node.add_node(parse(input))
    for d in range(n_meta):
        node.add_meta(input.pop(0))
    return node


def part_I(input):
    start_time = time.time()
    print('Part I')
    root = parse(input)
    print(root.calculate_meta())
    print('Finished in {} seconds\n'.format(time.time()-start_time))


def part_II(input):
    start_time = time.time()
    print('Part II')
    root = parse(input)
    print(root.calculate_value())
    print('Finished in {} seconds'.format(time.time()-start_time))


if __name__ == '__main__':
    args = parse_arguments()

    s = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2\n'
    s = parse_file(args.input)
    input = [int(x) for x in s.split(' ')]

    part_I(input)
    input = [int(x) for x in s.split(' ')]
    part_II(input)

