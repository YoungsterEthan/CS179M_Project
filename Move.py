# Data structure for move data
class Move:
    def __init__(self, m_t, m_f, ttm):
        self.m_to = m_t
        self.m_from = m_f
        self.time_to_move = ttm