from copy import deepcopy

import numpy as np
from matplotlib import pyplot as plt


class Vertex:
    def __init__(self, i, j, vertex_number, height):
        self.vertex_number = vertex_number
        self.height = height
        self.i = i
        self.j = j
        self.adjacent_spots = set()  # list of vertex numbers

    def __str__(self):
        return f"V{self.vertex_number}|{self.i,self.j}|{self.height} -> {self.adjacent_spots}"

    def __repr__(self):
        return self.__str__()


class Graph:
    def __init__(self, vertex_list, height_map):
        self.height_map = height_map
        for vertex in vertex_list:
            if vertex.height == 0:
                self.start = vertex.vertex_number
                vertex.height = get_height("z")
                self.height_map[vertex.i, vertex.j] = get_height("z")
            if vertex.height == 27:
                self.end = vertex.vertex_number
                self.height_map[vertex.i, vertex.j] = get_height("a")
                vertex.height = get_height("a")
            create_edges_for_connected_vertices(vertex, self.height_map)
        self.vertices = vertex_list

    def find_distances_from_start(self):
        # dijsktra
        source = self.start
        distances = [np.Infinity for _ in range(len(self.vertices))]
        previous_vertices = [None for _ in range(len(self.vertices))]
        distances[source] = 0
        queue = deepcopy(self.vertices)

        while len(queue) > 0:
            u = queue.pop(
                self._get_min_distance_vertex_index(queue, distances)
            )

            for adjacent_vertex in u.adjacent_spots:
                temp_distance = distances[u.vertex_number] + 1
                if temp_distance < distances[adjacent_vertex]:
                    distances[adjacent_vertex] = temp_distance
                    previous_vertices[adjacent_vertex] = u.vertex_number

        return distances, previous_vertices

    def _get_distance_and_previous_vertext(
        self, vertex, distance_list
    ):
        return distance_list[vertex.vertex_number]

    def _get_min_distance_vertex_index(self, queue, distances):
        existing_distances = [
            self._get_distance_and_previous_vertext(
                vertex, distances
            )
            for vertex in queue
        ]
        return existing_distances.index(min(existing_distances))


def create_edges_for_connected_vertices(vertex: Vertex, height_map):
    # can go up down left right
    # i is for line starting from top, j is for position in line starting from left
    max_i, max_j = height_map.shape
    # can go right only if not at the end
    if vertex.j != max_j - 1:
        r_adjacent_vertex = height_map[vertex.i, vertex.j + 1]
        if vertex.height + 1 >= r_adjacent_vertex:
            vertex.adjacent_spots.add(vertex.i * height_map.shape[1] + vertex.j + 1)
    # move left - only if not far left
    if vertex.j != 0:
        l_adjacent_vertex = height_map[vertex.i, vertex.j - 1]
        if vertex.height + 1 >= l_adjacent_vertex:
            vertex.adjacent_spots.add(vertex.i * height_map.shape[1] + vertex.j - 1)

    # move up - ya know the drill
    if vertex.i != 0:
        u_adjacent_vertex = height_map[vertex.i - 1, vertex.j]
        if vertex.height + 1 >= u_adjacent_vertex:
            vertex.adjacent_spots.add((vertex.i - 1) * height_map.shape[1] + vertex.j)

    # move down - what a surprise
    if vertex.i != max_i - 1:
        d_adjacent_vertex = height_map[vertex.i + 1, vertex.j]
        if vertex.height + 1 >= d_adjacent_vertex:
            vertex.adjacent_spots.add((vertex.i + 1) * height_map.shape[1] + vertex.j)


def get_height_first(letter: str) -> int:
    if letter == "S":
        return 0
    elif letter == "E":
        return 27
    else:
        return ord(letter) - (ord("a") - 1)


def get_height(letter: str) -> int:
    if letter == "S":
        return abs(ord("a") - (ord("z")) - 1)
    elif letter == "E":
        return 0
    else:
        return abs(ord(letter) - (ord("z") + 1))


def convert_input_to_height_map(filename):
    with open(filename) as f:
        height_map = [list(map(get_height, list(line.strip()))) for line in f]
    return np.array(height_map)


def get_vertex_list_and_height_map_from_file(filename):
    with open(filename):
        height_map = convert_input_to_height_map(filename)
    return [
        Vertex(i, j, i * height_map.shape[1] + j, height_map[i, j])
        for i in range(height_map.shape[0])
        for j in range(height_map.shape[1])
    ], height_map


if __name__ == "__main__":

    filename = "input.dat"
    # filename = "test_input.dat"
    g = Graph(*get_vertex_list_and_height_map_from_file(filename))
    res = g.find_distances_from_start()
    possible_beginnings = [vertex.vertex_number for vertex in g.vertices if (vertex.height == 26)] # and (vertex.i == 0 or vertex.j == 0 or vertex.i == g.height_map.shape[0]-1 or vertex.j == g.height_map.shape[1]-1))]
    shortest_path_index = res[0].index(min([res[0][i] for i in possible_beginnings]))
    print(res[0][shortest_path_index])
    prev_vertex = res[1][shortest_path_index]
    path = []
    # build path
    while prev_vertex != None:
        path.append(prev_vertex)
        prev_vertex = res[1][prev_vertex]
    # highlight path on height map
    for vertex in path:
        i, j = g.vertices[vertex].i, g.vertices[vertex].j
        g.height_map[i, j] = 60

    plt.imshow(g.height_map)
    plt.imsave("result2.png", g.height_map)
    plt.show()
