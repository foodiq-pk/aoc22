def interval_overlaps(first, second):
    return (first[0] >= second[0] and first[1] <= second[1]) or (
        first[1] >= second[0] and first[0] <= second[1]
    )


# first assigment
def interval_is_in_other(first, second):
    return first[0] >= second[0] and first[1] <= second[1]


def one_contains_other_or_vice_versa(first, second):
    return any((interval_overlaps(first, second), interval_overlaps(second, first)))


def find_included_intervals_sum(filename):
    with open(filename) as f:
        inputs = [
            list(
                map(
                    lambda y: list(map(lambda z: int(z), y)),
                    list(map(lambda x: x.split("-"), ranges.split(","))),
                )
            )
            for ranges in f.read().split("\n")
        ]
        return sum(
            (
                one_contains_other_or_vice_versa(first, second)
                for first, second in inputs
            )
        )


#
# ---2---4
# --1---3-
# ---2--3-


if __name__ == "__main__":
    print(find_included_intervals_sum("test_input.dat"))
    print(find_included_intervals_sum("input.dat"))
