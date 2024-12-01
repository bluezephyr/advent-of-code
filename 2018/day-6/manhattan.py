#!/usr/bin/env python3
import argparse
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 6')
    parser.add_argument('input', help='File name for the input to parse')
    return parser.parse_args()


def parse_file(filename):
    """
    Parse the input file, line by line, and return a list of all the items.
    """
    item_list = []
    with open(args.input) as f:
        for item in f.readlines():
            x, y = item.split(',')
            item_list.append((int(x.strip()), int(y.strip())))
    return item_list


def distance(item1, item2):
    dx = abs(item1[0]-item2[0])
    dy = abs(item1[1]-item2[1])
    return dx+dy


def calculate_area(input):
    min_x = min([i[0] for i in input])
    max_x = max([i[0] for i in input])
    min_y = min([i[1] for i in input])
    max_y = max([i[1] for i in input])
    return max_x, max_y, min_x, min_y


def part_I(input):
    start_time = time.time()
    print('Part I')
    max_x, max_y, min_x, min_y = calculate_area(input)
    area = dict()

    for item in input:
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                d = distance(item, (x,y))
                try:
                    c_dist = area[(x,y)][0]
                    if c_dist > d:
                        # Replace with the new item as owner
                        area[(x,y)] = (d, item)
                    if c_dist == d:
                        # Same as previous - replace with None as owner
                        area[(x,y)] = (d, None)

                except KeyError:
                    # First item - store it as owner
                    area[(x,y)] = (d, item)

    largest_a = 0
    for item in input:
        # count number of squares in the area owned by item
        a = [i[1] for i in area.values()].count(item)
        if a > largest_a:
            largest_a = a

    print('Largest area is {}'.format(largest_a))
    print('Finished in {} seconds\n'.format(time.time()-start_time))



def part_II(input):
    start_time = time.time()
    print('Part II')
    max_x, max_y, min_x, min_y = calculate_area(input)
    area = dict()

    for item in input:
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                d = distance(item, (x,y))
                try:
                    area[(x,y)] += d
                except KeyError:
                    # First item - store its value
                    area[(x,y)] = d

    # count number of squares in the area with sum less than 10000
    print([i<10000 for i in area.values()].count(True))


    print('Finished in {} seconds'.format(time.time()-start_time))


if __name__ == '__main__':
    args = parse_arguments()

    input = parse_file(args.input)
    #input = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]

    print(input)
    part_I(input)
    part_II(input)

