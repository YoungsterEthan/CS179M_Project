## Data structure for container data
class ContainerData:
    def __init__(self, name: str = "UNUSED", weight: int = 0):
        self.name = name
        self.weight = weight

    def __str__(self):
        if self.name == "UNUSED":
            return "crane"
        c = 5-len(str(self.weight))

        return self.name + " {" + "0"*c + str(self.weight) + "}"
    
    def __eq__(self, other):
        if not isinstance(other, ContainerData):
            return False
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)