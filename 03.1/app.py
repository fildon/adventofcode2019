from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

class WirePath:
    def __init__(self, input_string):
        self.directions = input_string.strip().split(',')
        self.positions = self.get_positions()

    def get_positions(self):
        current_position = Point(0, 0)
        positions = dict()
        for direction in self.directions:
            heading = {
                'U': Point(0, 1),
                'D': Point(0, -1),
                'L': Point(-1, 0),
                'R': Point(1, 0)
            }[direction[0]]
            distance = int(direction[1:])
            for _ in range(distance):
                current_position = Point(
                    current_position.x + heading.x,
                    current_position.y + heading.y
                )
                if current_position.x not in positions:
                    positions[current_position.x] = set([])
                positions[current_position.x].add(current_position.y)
        return positions

    def distance_to_nearest_intersection(self, wire):
        return min(
            map(
                lambda i: abs(i.x) + abs(i.y),
                self.get_intersections(wire)
            )
        )

    def get_intersections(self, wire):
        intersections = []
        for x in iter(self.positions):
            if x not in wire.positions:
                continue
            intersecting_y_at_this_x = self.positions[x].intersection(wire.positions[x])
            intersections += [Point(x, y) for y in intersecting_y_at_this_x]
        return intersections


file = open('input.txt', 'r')
wire1 = WirePath(file.readline())
wire2 = WirePath(file.readline())

print(wire1.distance_to_nearest_intersection(wire2))
