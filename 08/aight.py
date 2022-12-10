import numpy as np


def is_tree_visible(index1, index2, matrix):
    # outside
    if (
        index1 == 0
        or index2 == 0
        or index1 == matrix.shape[0] - 1
        or index2 == matrix.shape[1] - 1
    ):
        return 1
    # inside
    else:
        tree = matrix[index1, index2]
        # print(tree, index1, index2)
        # visible top
        top = max(matrix[:index1, index2]) < tree
        # print(matrix[:index1, index2])
        # visible left
        left = max(matrix[index1, :index2]) < tree
        # print(matrix[index1, :index2])
        # visible right
        right = max(matrix[index1, index2 + 1 :]) < tree
        # print(matrix[index1, index2+1:])
        # visible bottom
        bottom = max(matrix[index1 + 1 :, index2]) < tree
        # print(matrix[index1+1:, index2])
        # print()
        return int(any([top, left, right, bottom]))


def tree_score(index1, index2, matrix):
    tree = matrix[index1, index2]
    # visible top
    top = matrix[:index1, index2][::-1]
    top_view_score = get_view_distance(top, tree)
    # visible left
    left = matrix[index1, :index2][::-1]
    left_view_score = get_view_distance(left, tree)
    # visible right
    right = matrix[index1, index2 + 1 :]
    right_view_score = get_view_distance(right, tree)
    # visible bottom
    bottom = matrix[index1 + 1 :, index2]
    bottom_view_score = get_view_distance(bottom, tree)
    return top_view_score * left_view_score * right_view_score * bottom_view_score


def get_view_distance(trees, tree_height):
    if len(trees) == 0 or len(trees) == 1:
        return len(trees)
    elif max(trees) < tree_height:
        return len(trees)
    else:
        count = 0
        for tree in trees:
            count += 1
            if tree >= tree_height:
                return count
        return count


if __name__ == "__main__":
    print("test")
    with open("test_input.dat") as f:
        a = np.array([list(line.strip()) for line in f], dtype=int)
        print(a)
        print(a.shape)
        visible_trees = []
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                visible_trees.append([i, j]) if is_tree_visible(i, j, a) else None
        print(visible_trees)
        print(len(visible_trees))
        print(
            max(
                [
                    tree_score(i, j, a)
                    for i in range(a.shape[0])
                    for j in range(a.shape[1])
                ]
            )
        )

    print("input")
    with open("input.dat") as f:
        a = np.array([list(line.strip()) for line in f], dtype=int)
        print(a)
        print(a.shape)
        visible_trees = []
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                visible_trees.append([i, j]) if is_tree_visible(i, j, a) else None
        print(len(visible_trees))
        print(
            max(
                [
                    tree_score(i, j, a)
                    for i in range(a.shape[0])
                    for j in range(a.shape[1])
                ]
            )
        )
