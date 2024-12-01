#!/usr/bin/env python3
import argparse
import time
import datetime


class Guard():
    def __init__(self, guard_id):
        self.guard_id = guard_id
        self.asleep = []
        self.overlaps = {}

    def store_sleep_period(self, start, end):
        period = []
        period.extend(range(start.minute, end.minute))
        self.asleep.append(period)

    def get_total_sleep_time(self):
        sleep_time = 0
        for item in self.asleep:
            sleep_time += len(item)
        return sleep_time

    def _get_all_minutes(self):
        all_minutes = {}
        for period in self.asleep:
            for minute in period:
                try:
                    all_minutes[minute] = all_minutes[minute] + 1
                except KeyError:
                    all_minutes[minute] = 1
        return all_minutes

    def get_most_overlapping_minute(self):
        all_minutes = self._get_all_minutes()

        largest_value = 0
        largest_value_item = 0
        for item, value in all_minutes.items():
            if value > largest_value:
                largest_value = value
                largest_value_item = item

        return largest_value_item

    def calculate_all_overlaps(self):
        all_minutes = self._get_all_minutes()
        for item, value in all_minutes.items():
            if value > 1:
                self.overlaps[item] = value


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 4')
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


def parse_row_for_id(item):
    try:
        guard_id = item.split('#')[1].split(' ')[0]
        timestamp = datetime.datetime.strptime(item.split('[')[1].split(']')[0], '%Y-%m-%d %H:%M')
        return timestamp, guard_id
    except IndexError:
        return None, None


def parse_row_for_event(item):
    """
    Return event (falls_asleep or wakes_up) and time stamp for event
    """
    event = item.split(']')[1].strip()
    timestamp = datetime.datetime.strptime(item.split('[')[1].split(']')[0], '%Y-%m-%d %H:%M')
    return timestamp, event


def parse_guard_schedule(input):
    """
    Parse the guard schedule and return a dict of all the guards
    """
    all_guards = {}
    current_guard = None
    asleep = False
    for item in sorted(input):
        timestamp, guard_id = parse_row_for_id(item)

        if guard_id:
            # Guard shift
            asleep = False
            start_time = timestamp
            try:
                current_guard = all_guards[guard_id]
            except KeyError:
                current_guard = Guard(guard_id)
                all_guards[guard_id] = current_guard

        else:
            # Event
            timestamp, event = parse_row_for_event(item)
            if asleep and event == 'wakes up':
                asleep = False
                current_guard.store_sleep_period(start_time, timestamp)
            if not asleep and event == 'falls asleep':
                start_time = timestamp
                asleep = True
    return all_guards


def part_I(input):
    print('Part I')
    all_guards = parse_guard_schedule(input)

    most_sleeping_guard = None
    most_sleeping_time = 0
    for guard_id, guard in all_guards.items():
        print('Guard {} slept for {} minutes'.format(guard_id, guard.get_total_sleep_time()))
        sleep_time = guard.get_total_sleep_time()
        if sleep_time > most_sleeping_time:
            most_sleeping_guard = guard_id
            most_sleeping_time = sleep_time

    guard = all_guards[most_sleeping_guard]
    product = int(most_sleeping_guard)*guard.get_most_overlapping_minute()
    print('Most sleeping guard: {}'.format(most_sleeping_guard))
    print('Most overlapping minute: {}'.format(guard.get_most_overlapping_minute()))
    print('Product {} * {} = {}'.format(most_sleeping_guard, guard.get_most_overlapping_minute(), product))


def part_II(input):
    print('Part II')
    all_guards = parse_guard_schedule(input)

    largest_overlap_minute = 0
    largest_overlap_minute_value = 0
    largest_overlap_minute_guard = None
    for guard_id, guard in all_guards.items():
        guard.calculate_all_overlaps()
        for overlap, value in guard.overlaps.items():
            if value > largest_overlap_minute_value:
                largest_overlap_minute_value = value
                largest_overlap_minute = overlap
                largest_overlap_minute_guard = guard_id

        print('#{} - {}'.format(guard_id, guard.overlaps))

    print('Largest overlap value: {} at minute {} for guard #{}'.format(
        largest_overlap_minute_value, largest_overlap_minute, largest_overlap_minute_guard))
    print('Product {} * {} = {}'.format(int(largest_overlap_minute_guard), largest_overlap_minute,
                                        int(largest_overlap_minute_guard)*largest_overlap_minute))


if __name__ == '__main__':
    start_time = time.time()
    args = parse_arguments()

    test_input = [
        '[1518-11-01 00:25] wakes up              ',
        '[1518-11-01 00:05] falls asleep          ',
        '[1518-11-02 00:40] falls asleep          ',
        '[1518-11-01 00:55] wakes up              ',
        '[1518-11-01 23:58] Guard #99 begins shift',
        '[1518-11-02 00:50] wakes up              ',
        '[1518-11-03 00:05] Guard #10 begins shift',
        '[1518-11-03 00:24] falls asleep          ',
        '[1518-11-01 00:00] Guard #10 begins shift',
        '[1518-11-03 00:29] wakes up              ',
        '[1518-11-04 00:02] Guard #99 begins shift',
        '[1518-11-04 00:36] falls asleep          ',
        '[1518-11-04 00:46] wakes up              ',
        '[1518-11-05 00:03] Guard #99 begins shift',
        '[1518-11-05 00:45] falls asleep          ',
        '[1518-11-01 00:30] falls asleep          ',
        '[1518-11-05 00:55] wakes up              ']

    item_list = parse_file(args.input)

    part_I(item_list)
    #part_I(test_input)
    part_II(item_list)

    print('Finished in {} seconds'.format(time.process_time()))

