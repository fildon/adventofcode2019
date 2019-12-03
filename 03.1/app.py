from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

class WirePath:
    def __init__(self, input_string):
        self.path_set = []
        self.directions = input_string.strip().split(',')
        self.get_path_set()

    def get_path_set(self):
        current_position = Point(0, 0)
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
                self.path_set.append(current_position)
        self.path_set.sort(key = lambda p: 10000 * p.x + p.y)

    def distance_to_nearest_intersection(self, wire):
        return min(
            map(
                lambda i: abs(i.x) + abs(i.y),
                self.get_intersections(wire)
            )
        )

    def get_intersections(self, wire):
        intersections = []
        for pointA in self.path_set:
            for pointB in wire.path_set:
                if pointA.x == pointB.x and pointA.y == pointB.y:
                    intersections.append(pointA)
        return intersections


file = open('test1.txt', 'r')
wire1 = WirePath(file.readline())
wire2 = WirePath(file.readline())

print(wire1.distance_to_nearest_intersection(wire2))
