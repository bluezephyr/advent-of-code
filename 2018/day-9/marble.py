#!/usr/bin/env python3
import argparse
import collections
import time


class Game(object):
    def __init__(self):
        self.board = collections.deque()
        self.board.append(0)

    def play(self, marble):
        # Current marble is always at index 0.  Rotate deque to find next position.
        points = 0
        if marble % 23 == 0:
            points += marble
            self.board.rotate(7)
            points += self.board.popleft()
        else:
            self.board.rotate(-2)
            self.board.appendleft(marble)
        return points


class Player(object):
    def __init__(self, number):
        self.number = number
        self.points = 0


def parse_arguments():
    parser = argparse.ArgumentParser(description='Advent of code day 9')
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
    players = int(data.split(' ')[0])
    last_marble = int(data.split(' ')[6])
    return players, last_marble


def create_players(nbr_players):
    players = []
    for i in range(nbr_players):
        # Player number starts at 1
        player = Player(i+1)
        players.append(player)
    return players


def find_winner(players):
    max_points = 0
    leader = players[0]

    for player in players:
        if player.points > max_points:
            leader = player
            max_points = leader.points
    return leader


def play_game(last_marble, nbr_players):
    # Create new game
    game = Game()
    players = create_players(nbr_players)
    player_in_turn = iter(players)
    for marble in range(1, last_marble + 1):
        try:
            player = next(player_in_turn)
        except StopIteration:
            player_in_turn = iter(players)
            player = next(player_in_turn)
        player.points += game.play(marble)
    return players


def part_I(input_data):
    start_time = time.time()
    print('Part I')
    for line in input_data:
        nbr_players, last_marble = parse_input(line)
        print('{} players, last marble is {}'.format(nbr_players, last_marble))
        players = play_game(last_marble, nbr_players)
        winner = find_winner(players)
        print('Player {} wins with {} points'.format(winner.number, winner.points))

    print('Finished in {} seconds\n'.format(time.time()-start_time))


def part_II(input_data, previous_winner):
    start_time = time.time()
    print('Part II')
    for line in input_data:
        nbr_players, last_marble = parse_input(line)
        last_marble = last_marble*100
        print('{} players, last marble is {}'.format(nbr_players, last_marble))
        players = play_game(last_marble, nbr_players)

    winner = find_winner(players)
    print('Player {} wins with {} points'.format(winner.number, winner.points))
    print('Finished in {} seconds'.format(time.time()-start_time))


if __name__ == '__main__':
    args = parse_arguments()
    data = [
        '10 players; last marble is worth 1618 points: high score is 8317',
        '13 players; last marble is worth 7999 points: high score is 146373',
        '17 players; last marble is worth 1104 points: high score is 2764',
        '21 players; last marble is worth 6111 points: high score is 54718',
        '30 players; last marble is worth 5807 points: high score is 37305',
        ]

    data = parse_file(args.input)

    part_I(data)
    part_II(data, 137)

