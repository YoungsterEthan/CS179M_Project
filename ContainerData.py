## Data structure for container data
class ContainerData:
    def __init__(self, name = "UNUSED", weight = "00000"):
        self.name = name
        self.weight = weight

    def __str__(self):
        return self.name + " {" + self.weight + "}"