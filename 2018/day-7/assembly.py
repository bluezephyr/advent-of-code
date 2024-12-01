#!/usr/bin/env python3
import argparse
import time


class Workers(object):
    def __init__(self, number, time_to_build):
        self.time_to_build = time_to_build
        self.no_of_workers = number
        self.time_spent = 0
        self.ready_to_build = set()
        self.in_progress = []
        self.time_to_next_ready = 0

    def build(self):
        '''
        Use all workers (with items) to build until (at least) one item has been built
        :return: set of built items
        '''
        self.time_to_next_ready = min(x[1] for x in self.in_progress)
        done = []

        # All workers build on their items
        for i, _ in enumerate(self.in_progress):
            self.in_progress[i] = (self.in_progress[i][0], self.in_progress[i][1]-self.time_to_next_ready)
            if self.in_progress[i][1] == 0:
                done.append(self.in_progress[i][0])

        # Remove all done work from in progress list
        for item in self.in_progress:
            if item[0] in done:
                self.in_progress.remove(item)

        self.time_spent += self.time_to_next_ready
        return set(done)

    def add_items_to_build(self, items):
        self.ready_to_build = self.ready_to_build.union(items)

        if (self.ready_to_build):
            # Give work to as many workers as possible
            while self.ready_to_build and len(self.in_progress) < self.no_of_workers:
                # Get item with highest priority
                item = sorted(self.ready_to_build)[0]
                self.ready_to_build.remove(item)
                self.in_progress.append((item, ord(item)-ord('@')+self.time_to_build))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 7')
    parser.add_argument('input', help='File name for the input to parse')
    return parser.parse_args()


def parse_file(filename):
    """
    Parse the input file, line by line, and return a list of all the items.
    """
    item_list = []
    with open(args.input) as f:
        for item in f.readlines():
            item_list.append(item)
    return item_list


def create_dependencies(input):
    dep = {}
    all_steps = set()
    for item in input:
        depend_on = item.split('Step ')[1][:1]
        step = item.split('step ')[1][:1]
        all_steps.add(step)
        all_steps.add(depend_on)
        try:
            dep[step].append(depend_on)
        except KeyError:
            dep[step] = [depend_on]
    return set(sorted(all_steps)), dep


def reduce(dep, step):
    for key, value in dep.items():
        try:
            value.remove(step)
        except ValueError:
            pass


def pop_steps_without_dependencies(dep):
    free_steps = set()
    for key, value in dep.items():
        if value == []:
            free_steps.add(key)
    for key in free_steps:
        dep.pop(key)
    return free_steps


def part_I(input):
    start_time = time.time()
    print('Part I')
    all_steps, dep = create_dependencies(input)
    free_steps = all_steps-set(dep)
    assembled_steps = []

    while len(assembled_steps) < len(all_steps):
        step = sorted(free_steps)[0]
        free_steps.remove(step)
        assembled_steps.append(step)
        reduce(dep, step)
        free_steps = free_steps.union(pop_steps_without_dependencies(dep))

    print('Used steps: {}'.format(''.join(assembled_steps)))
    print('Finished in {} seconds\n'.format(time.time()-start_time))


def part_II(input):
    start_time = time.time()
    print('Part II')
    workers = Workers(5, 60)
    all_steps, dep = create_dependencies(input)
    ready_to_build = all_steps-set(dep)
    ready_to_assemble = set()
    assembled_steps = []

    while len(assembled_steps) < len(all_steps):
        workers.add_items_to_build(ready_to_build)
        ready_to_assemble = ready_to_assemble.union(workers.build())
        step = sorted(ready_to_assemble)[0]
        ready_to_assemble.remove(step)
        assembled_steps.append(step)
        reduce(dep, step)
        ready_to_build = pop_steps_without_dependencies(dep)

    print('Used steps: {}'.format(''.join(assembled_steps)))
    print('Used time to build: {} seconds'.format(workers.time_spent))
    print('Finished in {} seconds'.format(time.time()-start_time))


if __name__ == '__main__':
    args = parse_arguments()

    input = ['Step C must be finished before step A can begin.',
             'Step C must be finished before step F can begin.',
             'Step A must be finished before step B can begin.',
             'Step A must be finished before step D can begin.',
             'Step B must be finished before step E can begin.',
             'Step D must be finished before step E can begin.',
             'Step F must be finished before step E can begin.']
    input = parse_file(args.input)

    part_I(input)
    part_II(input)

