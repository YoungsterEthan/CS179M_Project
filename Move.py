from ContainerData import ContainerData
# Data structure for move data
class Move:
    def __init__(self, m_from, m_to, ttm, container):
        self.m_from = m_from
        self.m_to = m_to
        self.time_to_move = ttm
        self.container = container

    def __str__(self):
        return "Move " + str(self.container) + " from " + self.m_from + " to " + self.m_to + " in " + str(self.time_to_move) + " minutes"