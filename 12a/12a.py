from functools import reduce
from itertools import combinations


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



class Moon:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector(0, 0, 0)

    def __repr__(self):
        return f'Moon({self.position}, {self.velocity})'

    def apply_velocity(self):
        self.position = self.position.add(self.velocity)

    def potential_energy(self):
        return self.position.sum_absolute()

    def kinetic_energy(self):
        return self.velocity.sum_absolute()

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def apply_gravity_of(self, moon):
        self.velocity = self.velocity.add(self.position.unit_differences(moon.position))


class Simulation:
    def __init__(self, moons):
        self.moons = moons
    
    def __repr__(self):
        return f'Simulation({self.moons})'

    def step(self, n = 1):
        for _ in range(n):
            self.update_velocities()
            self.update_positions()

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

    def sum_total_energy(self):
        return reduce(
            lambda m, n: m + n,
            map(lambda moon: moon.total_energy(), self.moons),
        )


test1_moons = [
    Moon(Vector(-1, 0, 2)),
    Moon(Vector(2, -10, -7)),
    Moon(Vector(4, -8, 8)),
    Moon(Vector(3, 5, -1))
]

test2_moons = [
    Moon(Vector(-8, 10, 0)),
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

simulation = Simulation(input_moons)
simulation.step(1000)
print(simulation.sum_total_energy())
# SOLVED 5517
