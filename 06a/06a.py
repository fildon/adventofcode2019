class OrbitalTree:
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.orbits = list(map(lambda line: line.split(')'), file.read().strip().split('\n')))
        self.scores = dict({'COM': 0})

    def get_orbital_score(self):
        score = 0
        while len(self.orbits) > 0:
            if self.orbits[0][0] in self.scores:
                score += self.scores[self.orbits[0][0]] + 1
                self.scores[self.orbits[0][1]] = self.scores[self.orbits[0][0]] + 1
                self.orbits = self.orbits[1:]
            else:
                self.orbits = self.orbits[1:] + self.orbits[:1]
        return score


print(OrbitalTree('input.txt').get_orbital_score())
