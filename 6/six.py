def get_marker_index(sequence, consecutive_letters):
    for i in range(0, len(sequence) - consecutive_letters):
        if len(set(sequence[i : i + consecutive_letters])) == consecutive_letters:
            print(i + consecutive_letters)
            break


if __name__ == "__main__":
    print("test1 - 7 5 6 10 11")
    with open("test_input.dat") as f:
        for line in f:
            get_marker_index(line.strip(), 4)

    print("input1")
    with open("input.dat") as f:
        for line in f:
            get_marker_index(line.strip(), 4)

    print("test2 - 19 23 23 29 26")
    with open("test_input.dat") as f:
        for line in f:
            get_marker_index(line.strip(), 14)

    print("input2")
    with open("input.dat") as f:
        for line in f:
            get_marker_index(line.strip(), 14)
