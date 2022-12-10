if __name__ == "__main__":

    elves_carry = []
    with open("input.dat") as f:
        amount = 0
        for line in f:
            if line == "\n":
                elves_carry.append(amount)
                amount = 0
            else:
                amount += int(line)
    elves_carry.sort()
    print(sum(elves_carry[-3:]))
