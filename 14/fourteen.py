import os
from typing import NoReturn

import imageio as imageio
import numpy as np
from matplotlib import pyplot as plt


class SandGrain:
    def __init__(self, location_x, location_y):
        self.location_x = location_x
        self.location_y = location_y
        self.resting = False

    def __str__(self):
        return f"GRAIN [{self.location_x}, {self.location_y} - {'resting' if self.resting else 'falling'}]"


class Scan:
    FLOOR_OFFSET = 1
    ENTRYPOINT_X = 500
    ENTRYPOINT_Y = 0

    def __init__(self, filename):
        # build_scan_from_file
        points = set()
        with open(filename) as f:
            for line in f:
                points = points.union(
                    self._create_structure_piece(self._parse_scan_line(line))
                )
        xs, ys = zip(*points)

        self.boundary_y = max(ys)
        self.boundary_x_min = min(xs)
        self.boundary_x_max = max(xs)
        self.structure = points
        self.active_grain: SandGrain | None = None
        self.resting_grains: list[SandGrain] = []

    def get_or_create_new_grain(self) -> SandGrain:
        if self.active_grain:
            return self.active_grain
        else:
            self.active_grain = SandGrain(self.ENTRYPOINT_X, self.ENTRYPOINT_Y)
            return self.active_grain

    def simulate_grain_step(self, floor=False) -> NoReturn:
        if (
            floor
            and self.active_grain.location_y == self.boundary_y + self.FLOOR_OFFSET
        ):
            self.resting_grains.append(self.active_grain)
            self.structure.add(
                (self.active_grain.location_x, self.active_grain.location_y)
            )
            self.active_grain.resting = True
            self.active_grain = None
        elif (
            not (self.active_grain.location_x, self.active_grain.location_y + 1)
            in self.structure
        ):
            self.active_grain.location_y += 1
        elif (
            not (self.active_grain.location_x - 1, self.active_grain.location_y + 1)
            in self.structure
        ):
            self.active_grain.location_y += 1
            self.active_grain.location_x -= 1
        elif (
            not (self.active_grain.location_x + 1, self.active_grain.location_y + 1)
            in self.structure
        ):
            self.active_grain.location_x += 1
            self.active_grain.location_y += 1
        elif self.active_grain.location_y == 0 and self.active_grain.location_x == 500:
            self.resting_grains.append(self.active_grain)
            self.structure.add(
            (self.active_grain.location_x, self.active_grain.location_y)
            )
            self.active_grain.resting = True
        else:
            self.resting_grains.append(self.active_grain)
            self.structure.add(
                (self.active_grain.location_x, self.active_grain.location_y)
            )
            self.active_grain.resting = True
            self.active_grain = None

    def simulate_sand_movement(self) -> NoReturn:
        while not self._grain_out_of_bounds_and_is_faaaalllin(
            self.get_or_create_new_grain()
        ):
            self.simulate_grain_step()
        self.active_grain = None

    def simulate_sand_movement_w_floow(self):
        while not self._grain_out_of_bounds_and_is_faaaalllin(
            self.get_or_create_new_grain(), floor=True
        ):
            self.simulate_grain_step(floor=True)

    def create_normalized_structure_img(self, filename, show_and_save=True):
        xs, ys = zip(*self.structure)
        max_x = max(xs)
        min_x = min(xs)
        max_y = max(ys)
        area = np.zeros(
            shape=(max_y+1, max_x - min_x + 1)
        )
        for point in self.structure:
            area[point[1], point[0] - min_x] = 5
        for grain in self.resting_grains:
            area[grain.location_y, grain.location_x - min_x] = 10

        # if self.active_grain and not self._grain_out_of_bounds_and_is_faaaalllin(
        #     self.active_grain
        # ):
        #     area[
        #         self.active_grain.location_y,
        #         self.active_grain.location_x - self.boundary_x_min,
        #     ] = 10

        area[0, 500 - min_x] = 9
        if show_and_save:
            plt.imsave(filename, area)
        return area
        # just for fun

    def create_animation_files(self, folder, step):
        i = 0
        if not os.path.exists(f"gif/{folder}"):
            os.mkdir(f"gif/{folder}")
        while not self._grain_out_of_bounds_and_is_faaaalllin(
            self.get_or_create_new_grain()
        ):
            self.simulate_grain_step()
            if i % step == 0:
                self.create_normalized_structure_img(f"gif/{folder}/gif_part_{i}.png")
            i += 1

    def _grain_out_of_bounds_and_is_faaaalllin(self, grain: SandGrain, floor=False):
        return grain.location_y > (
            (self.boundary_y + self.FLOOR_OFFSET) if floor else self.boundary_y
        ) or (grain.resting and grain.location_y == 0)

    @classmethod
    def _create_line(cls, start: tuple, end: tuple) -> set:
        line = set()
        line.add(start)
        line.add(end)
        if start[0] == end[0]:
            # exclude startpoint and add points in between
            for y in range(min(start[1], end[1]) + 1, max(start[1], end[1])):
                line.add((start[0], y))
        elif start[1] == end[1]:
            for x in range(min(start[0], end[0]) + 1, max(start[0], end[0])):
                line.add((x, start[1]))
        else:
            print(f"Invalid line with endpoints {start} - {end}")

        return line

    @classmethod
    def _create_structure_piece(cls, endpoints) -> set:
        structure = set()

        for i in range(len(endpoints) - 1):
            structure = structure.union(
                cls._create_line(endpoints[i], endpoints[i + 1])
            )

        return structure

    @classmethod
    def _parse_scan_line(cls, scan_line) -> list[tuple]:
        endpoints = list(
            map(
                lambda coords: tuple(
                    map(lambda coord: int(coord), (coords.strip().split(",")))
                ),
                scan_line.split("->"),
            )
        )
        return endpoints


# also not part of solution but some nonsense visualisation
def combine_into_gif(folder, filename, duration):
    filenames = os.listdir(f"gif/{folder}")
    filenames.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
    print(filenames[0:10])
    with imageio.get_writer(
        filename, mode="I", duration=duration / len(filenames)
    ) as writer:
        for filename in filenames:
            image = imageio.imread(f"gif/{folder}/{filename}")
            writer.append_data(image)


if __name__ == "__main__":
    s = Scan("test_input")
    # s.create_normalized_structure_img("test_1_initial.png")
    s.simulate_sand_movement()
    # s.create_normalized_structure_img("test_1_final.png")
    print(len(s.resting_grains))
    # #
    # s = Scan("inp.dat")
    # # s.create_normalized_structure_img("inp_initial.png")
    # s.simulate_sand_movement()
    # # s.create_normalized_structure_img("inp_simulated.png")
    # print(len(s.resting_grains))

    # part 2
    s = Scan("test_input")
    # s.create_normalized_structure_img("test_2_initial.png")
    s.simulate_sand_movement_w_floow()
    # s.create_normalized_structure_img("test_2_final.png")
    print(len(s.resting_grains))

    s = Scan("inp.dat")
    # s.create_normalized_structure_img("inp2_initial.png")
    s.simulate_sand_movement_w_floow()
    # s.create_normalized_structure_img("inp2_simulated.png")
    print(len(s.resting_grains))
