import re
from dataclasses import dataclass
from typing import List, NoReturn


@dataclass
class Crate:
    label: str

    def __str__(self):
        return f"[{self.label}]"

    def __repr__(self):
        return f"[{self.label}]"


class CrateColumn:
    def __init__(self, label):
        self.label = label
        self.crates = []

    def add_crate(self, crate: Crate) -> NoReturn:
        self.crates.append(crate)

    def pick_crate(self) -> Crate:
        return self.crates.pop()

    def __str__(self):
        return f"{self.label} - {''.join([str(crate) for crate in self.crates]) if self.crates else '|'}"

    def __repr__(self):
        return f"{self.label} - {''.join([str(crate) for crate in self.crates]) if self.crates else '|'}"


class Storage:
    size: int
    columns: List[CrateColumn]

    def display(self):
        layers = [
            " ".join(
                [
                    column.crates[i].__str__() if len(column.crates) - 1 >= i else "   "
                    for column in self.columns
                ]
            )
            for i in range(len(self.columns))
        ]
        for layer in layers.__reversed__():
            print(layer)
        print(f" {'   '.join([c.label for c in self.columns])} ")

    def get_top_crates(self) -> str:
        return f"{''.join(col.pick_crate().label for col in self.columns)}"

    def build(self, filename) -> NoReturn:
        with open(filename) as f:
            layers = [layer for layer in f]
            column_labels = layers.pop().strip().split("   ")
            self.size = len(column_labels)
            self.columns = [CrateColumn(column_label) for column_label in column_labels]
            for layer in layers.__reversed__():
                for column, box_label in zip(
                    self.columns, self._get_boxes_in_layer(layer)
                ):
                    if box_label.strip():
                        column.add_crate(Crate(box_label))

    def _get_boxes_in_layer(self, layer):
        return layer[1::4]


class Crane:
    def __init__(self, stackable, storage: Storage):
        self.stackable = stackable
        self.storage = storage

    def move_crate(
        self, origin: int, destination: int, suppress_display=False
    ) -> NoReturn:
        self.storage.columns[destination - 1].add_crate(
            self.storage.columns[origin - 1].pick_crate()
        )
        if not suppress_display:
            self.storage.display()

    def move_crates(
        self, origin, destination, amount, suppress_display=False
    ) -> NoReturn:
        if self.stackable:
            magazine = []
            for i in range(amount):
                magazine.append(self.storage.columns[origin - 1].pick_crate())
            for crate in magazine.__reversed__():
                self.storage.columns[destination - 1].add_crate(crate)
        else:
            for i in range(amount):
                self.move_crate(origin, destination, True)
        if not suppress_display:
            self.storage.display()

    def execute_move_order(self, order, suppress_display=False) -> NoReturn:
        amount, origin, destination = map(lambda x: int(x), re.findall(r"\d+", order))
        self.move_crates(origin, destination, amount, True)
        if not suppress_display:
            self.storage.display()

    def execute_move_orders_from_file(self, filename) -> NoReturn:
        with open(filename) as f:
            for line in f:
                self.execute_move_order(line.strip("\n"), True)
        self.storage.display()


if __name__ == "__main__":
    print("No Stacking - example")
    s = Storage()
    s.build("boxes_test_input.dat")
    s.display()
    print()
    crane = Crane(False, s)
    crane.execute_move_orders_from_file("moves_test_input.dat")
    print(crane.storage.get_top_crates())
    print()
    print("Stacking - example")
    s = Storage()
    s.build("boxes_test_input.dat")
    s.display()
    print()
    crane = Crane(True, s)
    crane.execute_move_orders_from_file("moves_test_input.dat")
    print(crane.storage.get_top_crates())

    print()
    print("No stacking")
    s = Storage()
    s.build("boxes_input.dat")
    s.display()
    print()
    crane = Crane(False, s)
    crane.execute_move_orders_from_file("moves_input.dat")
    print(crane.storage.get_top_crates())
    print()
    print("Stacking")
    s = Storage()
    s.build("boxes_input.dat")
    s.display()
    print()
    crane = Crane(True, s)
    crane.execute_move_orders_from_file("moves_input.dat")
    print(crane.storage.get_top_crates())
