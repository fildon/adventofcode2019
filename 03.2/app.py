from collections import namedtuple
Point = namedtuple('Point', ['x', 'y', 'steps'])

class WirePath:
    def __init__(self, input_string):
        self.directions = input_string.strip().split(',')
        self.positions = self.get_positions()

    def get_positions(self):
        current_position = Point(0, 0, 0)
        positions = dict()
        for direction in self.directions:
            heading = {
                'U': Point(0, 1, 0),
                'D': Point(0, -1, 0),
                'L': Point(-1, 0, 0),
                'R': Point(1, 0, 0)
            }[direction[0]]
            distance = int(direction[1:])
            for _ in range(distance):
                current_position = Point(
                    current_position.x + heading.x,
                    current_position.y + heading.y,
                    current_position.steps + 1
                )
                if current_position.x not in positions:
                    positions[current_position.x] = dict()
                if current_position.y in positions[current_position.x]:
                    # Skips this x-y since it's already been registered at a lower step value
                    continue
                positions[current_position.x][current_position.y] = current_position.steps
        return positions

    def distance_to_nearest_intersection(self, wire):
        return min(
            map(
                lambda i: i.steps,
                self.get_intersections(wire)
            )
        )

    def get_intersections(self, wire):
        intersections = []
        for x in iter(self.positions):
            if x not in wire.positions:
                continue
            for y in self.positions[x]:
                if y not in wire.positions[x]:
                    continue
                intersections.append(Point(x, y, self.positions[x][y] + wire.positions[x][y]))
        return intersections


file = open('input.txt', 'r')
wire1 = WirePath(file.readline())
wire2 = WirePath(file.readline())

print(wire1.distance_to_nearest_intersection(wire2))
