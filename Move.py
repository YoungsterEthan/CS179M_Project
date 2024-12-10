from ContainerData import ContainerData
from Load_Balance.Position import Position
# Data structure for move data
class Move:
    def __init__(self, m_from: Position, m_to: Position, ttm: int, container: ContainerData = None):
        self.m_from = m_from
        self.m_to = m_to
        self.time_to_move = ttm
        if container == None:
            self.container = ContainerData()
        else:
            self.container = container

    def __str__(self):
        return "Move " + str(self.container) + " from " + str(self.m_from) + " to " + str(self.m_to) + " in " + str(self.time_to_move) + " minutes"
    
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.m_from == other.m_from and self.m_to == other.m_to and self.time_to_move == other.time_to_move and self.container == other.container