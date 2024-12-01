#!/usr/bin/python3
"""Day 2"""

# A - Rock, B - Paper, C - Scissors
# X - Rock, Y - Paper, Z - Scissors
# X - Lose, Y - Draw, Z - Win

game = {'A X': 'Draw', 'A Y': 'Win', 'A Z': 'Lose',
        'B X': 'Lose', 'B Y': 'Draw', 'B Z': 'Win',
        'C X': 'Win', 'C Y': 'Lose', 'C Z': 'Draw'}

response = {'X': 'Lose', 'Y': 'Draw', 'Z': 'Win'}
points_game = {'Win': 6, 'Draw': 3, 'Lose': 0}
points_response = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}


def score(line):
    return points_game[game[line]] + points_response[line[2]]


def score_2(line):
    wanted_outcome = response[line[2]]

    s = [key for (key, value) in game.items() if
         value == wanted_outcome and key[0] == line[0]]
    score = points_game[wanted_outcome] + points_response[s[0][2]]
    print(f"{wanted_outcome} -> {s[0]}, {score}")
    return score


def calculate_total_score(filename):
    with open(filename, encoding='utf-8') as f:
        scores = []
        for line in f:
            scores.append(score(line.strip()))
    return sum(scores)


def calculate_part_two(filename):
    with open(filename, encoding='utf-8') as f:
        scores = []
        for line in f:
            scores.append(score_2(line.strip()))
    return sum(scores)


if __name__ == '__main__':
    print(f"Answer 1: {calculate_total_score('input.txt')}")

    print(f"Answer 2: {calculate_part_two('input.txt')}")
