class OrbitalTree:
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.orbits = list(map(lambda line: line.split(')'), file.read().strip().split('\n')))
        self.registered_bodies = dict({'COM': OrbitalBody('COM', None)})

    def build_orbital_tree(self):
        while len(self.orbits) > 0:
            if self.orbits[0][0] in self.registered_bodies:
                parent = self.registered_bodies[self.orbits[0][0]]
                child = OrbitalBody(self.orbits[0][1], parent)
                self.registered_bodies[self.orbits[0][1]] = child
                parent.children.append(child)
                self.orbits = self.orbits[1:]
            else:
                self.orbits = self.orbits[1:] + self.orbits[:1]

class OrbitalBody:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
    
    def get_lineage(self):
        if self.name == 'COM':
            return []
        return self.parent.get_lineage() + [self.parent.name]


tree = OrbitalTree('input.txt')
tree.build_orbital_tree()

you_lineage = set(tree.registered_bodies['YOU'].get_lineage())
san_lineage = set(tree.registered_bodies['SAN'].get_lineage())

print(len(you_lineage ^ san_lineage))
# SOLVED 277
