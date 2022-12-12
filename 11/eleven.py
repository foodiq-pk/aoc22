from math import prod


class Monkey:
    id: int
    items: []
    operation: str
    test: bool
    target_true: int
    traget_false: int
    items_seen: int

    def __init__(self, id, items, operation, test, target_true, target_false):
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.target_true = target_true
        self.target_false = target_false
        self.inspected_items = 0

    def make_operation(self, item):
        old = item
        return eval(self.operation)

    def __str__(self):
        return f"M {self.id} - {self.items} - targets: {self.target_true, self.target_false} - {self.operation}| {self.inspected_items}"


class Bussiness:
    def __init__(self, worry=False):
        self.monkeys = []
        self.worry = worry
        self.worry_function = lambda x: x // 3

    def play_round(self):
        for monkey in self.monkeys:
            for item in monkey.items:
                new_item = monkey.make_operation(item)
                new_item_worry_level_down = self.worry_function(new_item)
                target = (
                    monkey.target_true
                    if new_item_worry_level_down % monkey.test == 0
                    else monkey.target_false
                )
                # print(f"Monkey {monkey.id}")
                # print(f"  Item: {item} - {new_item} - {new_item_worry_level_down} -> {target}")
                self.monkeys[target].items.append(new_item_worry_level_down)

            monkey.inspected_items += len(monkey.items)
            monkey.items = []

    def play_rounds(self, rounds):
        for i in range(rounds):
            self.play_round()

    def build_bussiness(self, filename):
        with open(filename) as f:
            input_list = [
                list(map(str.strip, monkey.split("\n")))
                for monkey in f.read().split("\n\n")
            ]
            for monkey in input_list:
                self.monkeys.append(
                    Monkey(
                        id=int(monkey[0].split(" ")[-1].strip(":")),
                        items=list(map(int, monkey[1].split(":")[1].split(","))),
                        operation=monkey[2].split("=")[1].strip(),
                        test=int(monkey[3].split(" ")[-1]),
                        target_true=int(monkey[4].split(" ")[-1]),
                        target_false=int(monkey[5].split(" ")[-1]),
                    )
                )
            if self.worry:
                # To retain the ability to tell if the number is divisible by what the monkeys have we have to reduce
                # the size of the number to acceptable levels but also keep the information
                # since the operations are only + and * and we need to keep it only for the monkeys (divisors for each)
                # we can do modulo for the number by the product of divisors to keep it
                # (horrible attempt to explain modular arithmetics - congruence)
                self.worry_function = lambda x: x % prod(
                    [monkey.test for monkey in self.monkeys]
                )

    def get_active_monkeys_sum(self):
        activity = [monkey.inspected_items for monkey in self.monkeys]
        activity.sort()
        return activity[-2] * activity[-1]

    def display(self):
        print("Bussiness")
        for monkey in self.monkeys:
            print(monkey)


if __name__ == "__main__":
    print("test - normal")
    b = Bussiness()
    b.build_bussiness("test_input.dat")
    b.display()
    b.play_rounds(20)
    b.display()
    print(b.get_active_monkeys_sum())

    print("test - worried")
    b = Bussiness(worry=True)
    b.build_bussiness("test_input.dat")
    b.display()
    b.play_rounds(10000)
    b.display()
    print(b.get_active_monkeys_sum())

    print("inp - normal")
    b2 = Bussiness()
    b2.build_bussiness("input.dat")
    b2.display()
    b2.play_rounds(20)
    b2.display()
    print(b2.get_active_monkeys_sum())

    print("inp - worried")
    b2 = Bussiness(worry=True)
    b2.build_bussiness("input.dat")
    b2.display()
    b2.play_rounds(10000)
    b2.display()
    print(b2.get_active_monkeys_sum())
