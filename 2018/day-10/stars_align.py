#!/usr/bin/env python3
import argparse
import time
import re


class Star():
    def __init__(self, definition):
        data = re.findall(r'(-?\d+)', definition)
        self.x = int(data[0])
        self.y = int(data[1])
        self.dx = int(data[2])
        self.dy = int(data[3])

    def move(self, steps):
        self.x += self.dx * steps
        self.y += self.dy * steps

    def __repr__(self):
        return '<({}, {}) {} {}>'.format(self.x, self.y, self.dx, self.dy)

    def __lt__(self, other):
        if self.y < other.y:
            return True
        if self.y == other.y and self.x < other.x:
            return True
        return False

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 10')
    parser.add_argument('input', help='File name for the input to parse')
    return parser.parse_args()


def parse_file(filename):
    """
    Parse the input file, line by line, and return a list of all the items.
    """
    lines = []
    with open(args.input) as f:
        for item in f.readlines():
            lines.append(item[:-1])
        return lines


def parse_input(data):
    stars = []
    for data in data:
        star = Star(data)
        stars.append(star)
    return stars


def calculate_constellation_size(stars):
    min_x = stars[0].x
    min_y = stars[0].y
    max_x = stars[0].x
    max_y = stars[0].y
    for star in stars:
        min_x = min(min_x, star.x)
        min_y = min(min_y, star.y)
        max_x = max(max_x, star.x)
        max_y = max(max_y, star.y)
    return min_x, min_y, max_x, max_y


def move_stars(stars, steps):
    for star in stars:
        star.move(steps)


def print_lines(lines, max_x, max_y):
    for y in range(max_y):
        line = ''
        for x in range(max_x):
            line += '.'
        print(line)


def print_constellation(stars, max_x, max_y):
    lines = []
    line = []
    current_line = None
    for star in sorted(stars):
        if star.y != current_line:
            lines.append(line)
            current_line = star.y
            line = []
        line.append(star)
    print_lines(lines, max_x, max_y)


def print_const(stars, min_x, max_x, min_y, max_y):
    sorted_stars = iter(sorted(stars))
    star = next(sorted_stars)
    print('x   : {} -- {}'.format(min_x, max_x))
    for y in range(min_y, max_y+1):
        line = '{0: <4}:'.format(y)
        for x in range(min_x, max_x+1):
            if star and star.x == x and star.y == y:
                line += '#'
                try:
                    # Get next star that is not on the same location
                    next_star = next(sorted_stars)
                    while star.x == next_star.x and star.y == next_star.y:
                        next_star = next(sorted_stars)
                    star = next_star
                except StopIteration:
                    star = None
            else:
                line += '.'
        print(line)


def part_I(input_data):
    start_time = time.time()
    print('Part I')
    stars = parse_input(input_data)
    i = 0

    start_steps = 1
    start_steps = 10946
    move_stars(stars, start_steps)
    for i in range(5000):
        min_x, min_y, max_x, max_y = calculate_constellation_size(stars)
        if min_y>=0 and max_y-min_y<30 and max_x-min_x < 300:
            print('min_x:{}, max_x: {}, min_y:{}, max_y:{}'.format(min_x,max_x,min_y,max_y))
            print_const(stars, min_x, max_x, min_y, max_y)
            break
        move_stars(stars, 1)
    print('Finished in {} seconds\n'.format(time.time()-start_time))
    return i+start_steps


def part_II(input_data):
    start_time = time.time()
    print('Part II')
    print('Constellation found after {} seconds'.format(input_data))
    print('Finished in {} seconds'.format(time.time()-start_time))


if __name__ == '__main__':
    args = parse_arguments()
    data = [
        'position=< 9,  1> velocity=< 0,  2>',
        'position=< 7,  0> velocity=<-1,  0>',
        'position=< 3, -2> velocity=<-1,  1>',
        'position=< 6, 10> velocity=<-2, -1>',
        'position=< 2, -4> velocity=< 2,  2>',
        'position=<-6, 10> velocity=< 2, -2>',
        'position=< 1,  8> velocity=< 1, -1>',
        'position=< 1,  7> velocity=< 1,  0>',
        'position=<-3, 11> velocity=< 1, -2>',
        'position=< 7,  6> velocity=<-1, -1>',
        'position=<-2,  3> velocity=< 1,  0>',
        'position=<-4,  3> velocity=< 2,  0>',
        'position=<10, -3> velocity=<-1,  1>',
        'position=< 5, 11> velocity=< 1, -2>',
        'position=< 4,  7> velocity=< 0, -1>',
        'position=< 8, -2> velocity=< 0,  1>',
        'position=<15,  0> velocity=<-2,  0>',
        'position=< 1,  6> velocity=< 1,  0>',
        'position=< 8,  9> velocity=< 0, -1>',
        'position=< 3,  3> velocity=<-1,  1>',
        'position=< 0,  5> velocity=< 0, -1>',
        'position=<-2,  2> velocity=< 2,  0>',
        'position=< 5, -2> velocity=< 1,  2>',
        'position=< 1,  4> velocity=< 2,  1>',
        'position=<-2,  7> velocity=< 2, -2>',
        'position=< 3,  6> velocity=<-1, -1>',
        'position=< 5,  0> velocity=< 1,  0>',
        'position=<-6,  0> velocity=< 2,  0>',
        'position=< 5,  9> velocity=< 1, -2>',
        'position=<14,  7> velocity=<-2,  0>',
        'position=<-3,  6> velocity=< 2, -1>']

    data = parse_file(args.input)


    part_II(part_I(data))

