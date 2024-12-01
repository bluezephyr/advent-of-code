#!/usr/bin/env python3
import argparse
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 2 - letter counter')
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


def parse_box_id(id_string):
    """
    Return a tuple containing booleans if twice/three times letters were present in the id string.
    """
    count_2_found = False
    count_3_found = False
    id_count = {}

    for l in id_string:
        try:
            id_count[l] += 1
        except KeyError:
            id_count[l] = 1

    for key, value in id_count.items():
        if value == 2:
            count_2_found = True
        if value == 3:
            count_3_found = True

    return (count_2_found, count_3_found)


def part_I(id_list):
    number_of_two = 0
    number_of_three = 0

    for id_string in id_list:
        (two, three) = parse_box_id(id_string)
        if two:
            number_of_two += 1
        if three:
            number_of_three += 1

    print('Number of id:s with letter two times: {}'.format(number_of_two))
    print('Number of id:s with letter three times: {}'.format(number_of_three))
    print('Checksum (product): {}'.format(number_of_two*number_of_three))


def compare(id1, id2):
    """
    Return true if the ids differ by excatly one character.
    """
    diffs = 0
    for i, c in enumerate(id1):
        if c != id2[i]:
            diffs += 1
    return diffs == 1


def match_list(id_list):
    for i, id1 in enumerate(id_list):
        for id2 in id_list[i+1:]:
            if compare(id1, id2):
                return (id1, id2)
    return None


def find_matching_chars(id1, id2):
    matching = []
    for i, c1 in enumerate(id1):
        if c1 == id2[i]:
            matching.append(c1)
    return matching


def part_II(id_list):
    test = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']

    (match1, match2) = match_list(id_list)
    if match1 and match2:
        print('Found matching ids: {} - {}'.format(match1, match2))
        print('Common characters {}'.format(''.join(find_matching_chars(match1, match2))))
    else:
        print('No matching items found')



if __name__ == '__main__':
    start_time = time.time()
    args = parse_arguments()

    id_list = parse_file(args.input)
    part_I(id_list)
    part_II(id_list)

    print('Finished in {} seconds'.format(time.process_time()))

