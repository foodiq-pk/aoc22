class CRT:
    sprite_size = 3

    def __init__(self, screen_length):
        self.screen_length = screen_length
        self.image = []

    def write_pixel_value(self, cycle, sprite_position):
        # sprite index is offset by 1 from the cycle therefore for 3 size sprite we go sprite  pos, pos+1, pos+2
        if cycle % self.screen_length in range(
            sprite_position, sprite_position + self.sprite_size
        ):
            self.image.append("#")
        else:
            self.image.append(" ")

    def display(self):
        for line in [
            self.image[i: i + self.screen_length]
            for i in range(0, len(self.image), self.screen_length)
        ]:
            print(" ".join(line))


class Clock:
    def __init__(self, readouts, crt):
        self.cycle = 1
        self.outstanding_instructions = []
        self.register = 1
        self.readouts = readouts
        self.signals = []
        self.crt = crt

    def add_instruction(self, instruction):
        self.outstanding_instructions.append(instruction)

    def make_cycle(self):
        # print(f"cycle {self.cycle} - start, register - {self.register}")
        if self.cycle in self.readouts:
            self.signals.append(self.register * self.cycle)
        self.crt.write_pixel_value(cycle=self.cycle, sprite_position=self.register)
        for instruction in self.outstanding_instructions:
            if instruction.duration <= 1:
                self.outstanding_instructions.remove(instruction)
                self.register += instruction.value
            else:
                instruction.duration -= 1

        # print(f"cycle {self.cycle} - end, register - {self.register}")
        self.cycle += 1

    def execute_instruction(self, instruction):
        self.add_instruction(instruction)
        while self.outstanding_instructions:
            self.make_cycle()

    def get_readouts_signal_sum(self):
        return sum(self.signals)


class Instruction:
    def __init__(self, in_string):
        name, value = (
            in_string.split(" ") if in_string.startswith("a") else (in_string, 0)
        )
        if name == "noop":
            self.duration = 1
        elif name == "addx":
            self.duration = 2
        else:
            raise ValueError("Invalid instruction.")
        self.value = int(value)


if __name__ == "__main__":
    print("test")
    c = Clock([20, 60, 100, 140, 180, 220], CRT(40))
    with open("test_input2.dat") as f:
        for line in f:
            c.execute_instruction(Instruction(line.strip()))
    print(c.get_readouts_signal_sum())
    c.crt.display()

    print("input 1")
    c = Clock([20, 60, 100, 140, 180, 220], crt=CRT(40))
    with open("input.dat") as f:
        for line in f:
            c.execute_instruction(Instruction(line.strip()))
    print(c.get_readouts_signal_sum())
    c.crt.display()  # RKAZAJBR
