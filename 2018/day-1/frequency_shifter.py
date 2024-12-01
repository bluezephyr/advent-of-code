#!/usr/bin/env python3
import argparse
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 1 - frequence shifter')
    parser.add_argument('input', help='File name for the input to parse')
    return parser.parse_args()


def parse_file(filename):
    """
    Parse the input file, line by line, and return a list of all the items.
    """
    item_list = []
    with open(filename) as f:
        for item in f.readlines():
            item_list.append(int(item))
    return item_list


def find_duplicate_frequency(frequency_list):
    part_sums = []
    current_sum = 0
    part_sums.append(0)
    index = 0

    while True:
        for item in frequency_list:
            current_sum += item
            if current_sum in part_sums:
                part_sums.append(current_sum)
                print('Found duplicate at index: {} value {}'.format(index, current_sum))
                return
            part_sums.append(current_sum)
            index += 1


if __name__ == '__main__':
    args = parse_arguments()
    item_list = parse_file(args.input)

    item_list_test_1 = [+1, -1]
    item_list_test_2 = [+3, +3, +4, -2, -4]
    item_list_test_3 = [-6, +3, +8, +5, -6]
    item_list_test_4 = [+7, +7, -2, -7, -4]

    # Part I
    print('Resulting frequency: {}'.format(sum(item_list)))

    # Part II
    find_duplicate_frequency(item_list_test_1)
    find_duplicate_frequency(item_list_test_2)
    find_duplicate_frequency(item_list_test_3)
    find_duplicate_frequency(item_list_test_4)
    find_duplicate_frequency(item_list)

    print('Finished in {} seconds'.format(time.process_time()))
