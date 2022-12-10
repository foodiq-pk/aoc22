A = 1  # R
B = 2  # P
C = 3  # S

X = 1  # R
Y = 2  # P
Z = 3  # S
res_matrix = [[3, 0, 6], [6, 3, 0], [0, 6, 3]]
values = {"A": 1, "X": 1, "B": 2, "Y": 2, "C": 3, "Z": 3}

values_b = {"A": 1, "B": 2, "C": 3, "X": 0, "Y": 3, "Z": 6}

res_matrix_b = [[3, 1, 2], [1, 2, 3], [2, 3, 1]]


def find_player_selection(opponent, result):
    return values_b[result] + res_matrix_b[values[opponent] - 1][values[result] - 1]


def decide_result(opponent, player):
    return values[player] + res_matrix[values[player] - 1][values[opponent] - 1]


if __name__ == "__main__":
    print(decide_result("A", "Y"))
    print(decide_result("B", "X"))
    print(decide_result("C", "Z"))
    with open("input.dat") as f:
        print(sum(decide_result(*line.strip().split(" ")) for line in f))

    print(find_player_selection("A", "Y"))
    print(find_player_selection("B", "X"))
    print(find_player_selection("C", "Z"))

    with open("input.dat") as f:
        print(sum(find_player_selection(*line.strip().split(" ")) for line in f))
