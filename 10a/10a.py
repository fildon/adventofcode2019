import math

class AsteroidMap:
    def __init__(self, map_string_array):
        self.asteroid_map = map_string_array
        self.asteroids = set()
        for y in range(len(map_string_array)):
            for x in range(len(map_string_array[y])):
                if map_string_array[y][x] == '#':
                    self.asteroids.add(Asteroid(x, y))

    def get_best_site(self):
        return max(
            map(
                lambda asteroid: self.get_asteroid_score(asteroid),
                self.asteroids
            )
        )

    def get_asteroid_score(self, asteroid):
        return len(
            {other
             for other in self.asteroids
             if self.can_see(asteroid, other)})

    def can_see(self, asteroid1, asteroid2):
        # print(f'Can {asteroid1.x},{asteroid1.y} see {asteroid2.x},{asteroid2.y}?')
        x_diff = asteroid2.x - asteroid1.x
        y_diff = asteroid2.y - asteroid1.y
        if x_diff == 0 and y_diff == 0:
            # print('\tNo silly these two are the same')
            return False
        gcd = math.gcd(x_diff, y_diff)
        # print(f'\tGCD: {gcd}')
        x_step, y_step = int(x_diff / gcd), int(y_diff / gcd)
        # print(f'\tx_step: {x_step}, y_step: {y_step}')
        x_check = asteroid1.x + x_step
        y_check = asteroid1.y + y_step
        while x_check != asteroid2.x or y_check != asteroid2.y:
            # print(f'\tchecking {x_check},{y_check}')
            if self.asteroid_map[y_check][x_check] == '#':
                # print('\t\tObstructed!')
                return False
            # else:
            #     print('\t\tAll clear')
            x_check += x_step
            y_check += y_step
        # print(f'\tYes! These two can see each other')
        return True


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y


file = open('input.txt', "r")
asteroid_map = AsteroidMap(file.read().strip().split('\n'))
print(asteroid_map.get_best_site())
# SOLVED 329
