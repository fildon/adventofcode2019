from functools import reduce
from itertools import combinations
from math import gcd

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def sum_absolute(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def unit_differences(self, v):
        return Vector(
            -1 if v.x < self.x else 0 if v.x == self.x else 1,
            -1 if v.y < self.y else 0 if v.y == self.y else 1,
            -1 if v.z < self.z else 0 if v.z == self.z else 1,
        )
    
    def clone(self):
        return Vector(self.x, self.y, self.z)
    
    def equals(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


class Moon:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector(0, 0, 0)
        self.acceleration = Vector(0, 0, 0)
        self.start_pos = position.clone()

    def __repr__(self):
        return f'Moon({self.position}, {self.velocity})'

    def apply_velocity(self):
        self.position = self.position.add(self.velocity)

    def apply_gravity_of(self, moon):
        self.velocity = self.velocity.add(
            self.position.unit_differences(moon.position))


class Simulation:
    def __init__(self, moons):
        self.moons = moons
        self.steps = 0

    def __repr__(self):
        return f'Simulation({self.moons})'

    def find_repeat(self):
        x_repeat = None
        y_repeat = None
        z_repeat = None
        while not all([x_repeat, y_repeat, z_repeat]):
            self.step()
            if x_repeat == None and self.x_repeat():
                x_repeat = self.steps
                print(f'x repeats after: {x_repeat}')
            if y_repeat == None and self.y_repeat():
                y_repeat = self.steps
                print(f'y repeats after: {y_repeat}')
            if z_repeat == None and self.z_repeat():
                z_repeat = self.steps
                print(f'z repeats after: {z_repeat}')
        return self.lcm(self.lcm(x_repeat, y_repeat), z_repeat)
    
    def lcm(self, a, b):
        return abs(a * b) // gcd(a, b)

    def x_repeat(self):
        return all(map(lambda m: m.position.x == m.start_pos.x and m.velocity.x == 0, self.moons))

    def y_repeat(self):
        return all(map(lambda m: m.position.y == m.start_pos.y and m.velocity.y == 0, self.moons))

    def z_repeat(self):
        return all(map(lambda m: m.position.z == m.start_pos.z and m.velocity.z == 0, self.moons))
    
    def step(self):
        self.update_velocities()
        self.update_positions()
        self.steps += 1

    def update_velocities(self):
        for pair in self.all_pairs():
            self.update_velocity_pair(pair)

    def update_velocity_pair(self, moon_pair):
        moon_pair[0].apply_gravity_of(moon_pair[1])
        moon_pair[1].apply_gravity_of(moon_pair[0])

    def all_pairs(self):
        return list(combinations(self.moons, 2))

    def update_positions(self):
        for moon in self.moons:
            moon.apply_velocity()


test1_moons = [
    Moon(Vector(-1, 0, 2)),
    Moon(Vector(2, -10, -7)),
    Moon(Vector(4, -8, 8)),
    Moon(Vector(3, 5, -1))
]

test2_moons = [
    Moon(Vector(-8, -10, 0)),
    Moon(Vector(5, 5, 10)),
    Moon(Vector(2, -7, 3)),
    Moon(Vector(9, -8, -3))
]

input_moons = [
    Moon(Vector(-16, -1, -12)),
    Moon(Vector(0, -4, -17)),
    Moon(Vector(-11, 11, 0)),
    Moon(Vector(2, 2, -6))
]

import timeit

start = timeit.default_timer()

simulation = Simulation(input_moons)
repeat = simulation.find_repeat()
print(repeat)

stop = timeit.default_timer()

print(f'Time: ', stop - start)
