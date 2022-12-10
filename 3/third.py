from math import floor


def get_item_value(character):
    if character.islower():
        return ord(character) - (ord("a") - 1)
    else:
        return ord(character) - (ord("A") - 27)


def find_common_item_backpack(input_string):
    first = input_string[: floor(len(input_string) / 2)]
    second = input_string[floor(len(input_string) / 2) :]
    out = [item for item in first if item in second]
    assert list(out[0] * len(out)) == out
    return out[0]


def find_common_item_groups(input_strings):
    return [
        item
        for item in input_strings[0]
        if (item in input_strings[1] and item in input_strings[2])
    ][0]


def get_prioriy_of_bag(backpack_string):
    return get_item_value(find_common_item_backpack(backpack_string))


def get_priority_of_group(group_strings):
    return get_item_value(find_common_item_groups(group_strings))


def get_priority_sum_backpack(input_filename):
    with open(input_filename) as f:
        return sum([get_prioriy_of_bag(line) for line in f])


def get_priority_sum_groups(filename):
    with open(filename) as f:
        counter = 0
        groups = []
        group = []
        for line in f:
            group.append(line.strip())
            counter += 1
            if counter == 3:
                groups.append(group)
                group = []
                counter = 0

    return sum([get_priority_of_group(group) for group in groups])


if __name__ == "__main__":
    assert get_item_value("A") == 27
    assert get_item_value("a") == 1
    assert get_item_value("Z") == 52
    assert get_item_value("z") == 26

    print("first part")
    with open("test_inp") as f:
        for line in f:
            print(f"{find_common_item_backpack(line)}({get_prioriy_of_bag(line)})")

    print(f"Example priority: {get_priority_sum_backpack('test_inp')}")
    print(f"Priority: {get_priority_sum_backpack('input.dat')}")
    print("Second part")
    print(f"Example priority: {get_priority_sum_groups('test_inp')}")
    print(f"Priority: {get_priority_sum_groups('input.dat')}")
