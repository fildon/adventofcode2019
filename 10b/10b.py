import math

class AsteroidMap:
    def __init__(self, map_string_array):
        self.asteroid_map = map_string_array
        self.asteroids = set()
        for y in range(len(map_string_array)):
            for x in range(len(map_string_array[y])):
                if map_string_array[y][x] == '#':
                    self.asteroids.add(Asteroid(x, y))

    def can_see_list_lambda(self, view_from, condition_function):
        return [other for other in self.asteroids
            if self.can_see(view_from, other) and condition_function(other)]

    def can_see_list(self, view_from):
        return [other for other in self.asteroids
             if self.can_see(view_from, other)]

    def can_see_count(self, view_from):
        can_see = 0
        for asteroid in self.asteroids:
            if self.can_see(view_from, asteroid):
                can_see += 1
        return can_see

    def can_see(self, view_from, view_to):
        # print(f'Can {asteroid1.x},{asteroid1.y} see {asteroid2.x},{asteroid2.y}?')
        x_diff = view_to.x - view_from.x
        y_diff = view_to.y - view_from.y
        if x_diff == 0 and y_diff == 0:
            # print('\tNo silly these two are the same')
            return False
        gcd = math.gcd(x_diff, y_diff)
        # print(f'\tGCD: {gcd}')
        x_step, y_step = int(x_diff / gcd), int(y_diff / gcd)
        # print(f'\tx_step: {x_step}, y_step: {y_step}')
        x_check = view_from.x + x_step
        y_check = view_from.y + y_step
        while x_check != view_to.x or y_check != view_to.y:
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

# best site 25,31
# it can see 329

file = open('input.txt', "r")
asteroid_map = AsteroidMap(file.read().strip().split('\n'))
targets = asteroid_map.can_see_list(Asteroid(25, 31))

# 001 up
# 071 up_right
# 001 right
# 009 down_right
# 001 down
# 027 down_left
# 001 left
# CUMULATIVE TO THIS POINT: 111
# 218 up_left
# Therefore want 89th in up_left
quarter = asteroid_map.can_see_list_lambda(Asteroid(25, 31), lambda other: other.x < 25 and other.y < 31)
sorted_quarter = sorted(quarter, key=lambda a: ((31 - a.y)/(25 - a.x)))
print(list(map(lambda a: [a.x,a.y], sorted_quarter))[88])
# SOLVED 200th is at 5,12 which gives a solution of 512
