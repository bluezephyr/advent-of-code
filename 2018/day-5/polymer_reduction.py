#!/usr/bin/env python3
import argparse
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 5')
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


def next_non_reduced_char(i, reduced):
    index = i+1
    while index in reduced:
        index += 1
    return index


def find_first_reduction(input, reduced):
    if 0 in reduced:
        i = next_non_reduced_char(0, reduced)
    else:
        i = 0
    j = next_non_reduced_char(i, reduced)

    while i < len(input) and j < len(input):
        if abs(ord(input[i]) - ord(input[j])) == 32:
            return i, j
        i = next_non_reduced_char(i, reduced)
        j = next_non_reduced_char(i, reduced)

    # None found
    return None


def remove_reduced_chars(input, reduced):
    output = ''
    for i, c in enumerate(input):
        if not i in reduced:
            output += c
    return output


def reduce_input(input):
    reduced = set()
    reduced_tuple = set(find_first_reduction(input, reduced))
    while reduced_tuple:
        reduced |= set(reduced_tuple)
        reduced_tuple = find_first_reduction(input, reduced)
    reduced_input = remove_reduced_chars(input, reduced)
    return reduced_input


def part_I(input):
    print('Part I')
    print(input)

    reduced_input = reduce_input(input)
    print(reduced_input)
    print(len(reduced_input))


def remove_bad_chars(input, bad_chars):
    output = ''
    for c in input:
        if not c in bad_chars:
            output += c
    return output


def find_all_char_pairs(input):
    all_chars = set()
    for c in input:
        all_chars.add(c)
    all_chars = sorted(list(all_chars))
    return [c[0]+c[1] for c in zip(all_chars[:len(all_chars)//2], all_chars[len(all_chars)//2:])]


def part_II(input):
    print('Part II')

    all_char_pairs = find_all_char_pairs(input)
    print(all_char_pairs)

    shortest_reduction = len(input)
    shortest_reduction_char = None
    for pair in all_char_pairs:
        reduced_input = remove_bad_chars(input, pair)
        reduced_input = reduce_input(reduced_input)
        if len(reduced_input) < shortest_reduction:
            shortest_reduction = len(reduced_input)
            shortest_reduction_char = pair

    print("Shortest reduction: {}".format(shortest_reduction))
    print("Bad polymer: {}".format(shortest_reduction_char))


if __name__ == '__main__':
    start_time = time.time()
    args = parse_arguments()

    input = parse_file(args.input)[0]
    #input = 'dabAcCaCBAcCcaDA'

    part_I(input)
    part_II(input)

    print('Finished in {} seconds'.format(time.process_time()))

