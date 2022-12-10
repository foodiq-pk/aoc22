class Knot:
    def __init__(self, head, index):
        self.index = index
        self.locations = {(0, 0)}
        self.x = 0
        self.y = 0
        self.head = head

    def get_distance_to_head(self):
        return self.head.x - self.x, self.head.y - self.y

    def move_to_head(self):
        distance_x, distance_y = self.get_distance_to_head()
        # if distance is 0 - H on T, no move, same for when only 1 away (diagonal or
        if not (distance_x**2 + distance_y**2) ** 0.5 < 2:
            if distance_x == 0:
                # one is zero so there should be movement only in one axis towards the head
                self.y += 1 if distance_y > 0 else -1
            elif distance_y == 0:
                self.x += 1 if distance_x > 0 else -1
            else:
                # if not directly in column or row move diagonally, get signs from distance
                self.x += 1 if distance_x > 0 else -1
                self.y += 1 if distance_y > 0 else -1
        self.locations.add((self.x, self.y))

    def __str__(self):
        return f"K({self.index}) [{self.x}, {self.y}]"

    def __repr__(self):
        return self.__str__()

    def visited_locations(self):
        return len(self.locations)


class Head:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, direction):
        match direction:
            case "R":
                self.x += 1
            case "L":
                self.x -= 1
            case "U":
                self.y += 1
            case "D":
                self.y -= 1

    def __str__(self):
        return f"H [{self.x}, {self.y}]"

    def __repr__(self):
        return self.__str__()


class Rope:
    def __init__(self, head, nodes=2):  # min two nodes (1 head and 1 tail)
        self.head = head
        self.knots = [Knot(head, 1)]
        for i in range(2, nodes):
            self.knots.append(Knot(self.knots[-1], i))
        self.tail = self.knots[-1]

    def move_head(self, direction):
        self.head.move(direction)
        for knot in self.knots:
            knot.move_to_head()

    def move_head_distance(self, direction, distance):
        for i in range(distance):
            self.move_head(direction)

    def __str__(self):
        return f"{self.head} - {[knot for knot in self.knots]}"


if __name__ == "__main__":
    print("first")
    rope = Rope(Head())
    with open("input.dat") as f:
        for instruction in f:
            direction, distance = instruction.split(" ")
            rope.move_head_distance(direction, int(distance.strip()))
    print(rope.tail.visited_locations())

    print("second")
    print("test")

    r = Rope(head=Head(), nodes=10)
    with open("test_input2.dat") as f:
        for instruction in f:
            direction, distance = instruction.split(" ")
            r.move_head_distance(direction, int(distance.strip()))

    print(r.tail.visited_locations())
    print("input")
    r = Rope(head=Head(), nodes=10)
    with open("input.dat") as f:
        for instruction in f:
            direction, distance = instruction.split(" ")
            r.move_head_distance(direction, int(distance.strip()))

    print(r.tail.visited_locations())
