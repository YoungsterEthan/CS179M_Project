from consts import SHIP_HEIGHT, SHIP_WIDTH, SHIP_BUFF
from Load_Balance.State import State
from Load_Balance.Position import Position, Location
from Move import Move
import copy

'''
    State subclass for Balancing
    goal state is when left and right side of the ship weigh within 10% of each other
    next_states generates all possible states that can be reached from the current state
        states are generated by
            moving all containers on one half to the other half
            moving the crane back to the crane rest
            moving containers out of the buffers
    the heuristic of a state is
        the cost to move back to the crane rest
        the cost to move each container out of the buffers
        the distance to balance one half of the ship with the other
'''
class BalanceState(State):
    def __init__(self, manifest):
        super().__init__(manifest)
        self.left_weight = 0
        self.right_weight = 0
        self.total_weight = 0
        self.valid_range_small = 0
        self.valid_range_large = 0
        
        if manifest is not None:
            self.weigh_sides()
            self.total_weight = self.left_weight + self.right_weight
            self.valid_range_small = self.total_weight * 0.48
            self.valid_range_large = self.total_weight * 0.52


    def weigh_sides(self):
        self.left_weight = 0
        self.right_weight = 0
        for i in range(SHIP_HEIGHT):
            for j in range(SHIP_WIDTH):
                if self.ship[i][j]:
                    if j < SHIP_WIDTH//2:
                        self.left_weight += self.ship[i][j].weight
                    else:
                        self.right_weight += self.ship[i][j].weight


    def next_states(self):
        states = []
        self.move_containers_other_half(states) # generate states produced by moving containers from one side to the other
        self.clear_buffers(states)              # generate states produced by moving containers out of the buffers
        self.return_crane_rest(states)          # generate state produced by moving the crane back to the crane rest
        return states

    def calculate_h(self):
        self.weigh_sides()
        self.h = 0

        # best cost to move each container out of the buffers
        for pos in self.containers_in_buffers():
            self.h += self.search_from(pos, False, False)[1]

        # distance to move the crane to the crane rest
        if not self.crane_position.in_crane_rest():
            self.h += self.crane_position.move_to(Position(Location.CRANE_REST), apply_move=False)[1]

        if max(self.left_weight, self.right_weight)/max(1, min(self.left_weight, self.right_weight)) < 1.1:
            return

        l = self.left_weight
        r = self.right_weight

        # left side heavier
        if l > r:
            # move the heaviest containers to the right side of the ship until the right side is within the valid range
            visited = set()
            while not self.valid_range_small < r < self.valid_range_large:
                w = 0
                p = [-1,-1]
                for i in range(SHIP_HEIGHT+SHIP_BUFF):
                    for j in range(SHIP_WIDTH//2):
                        if self.ship[i][j] and r + self.ship[i][j].weight < self.valid_range_large and self.ship[i][j].weight > w and (i,j) not in visited:
                            w = self.ship[i][j].weight
                            p = [i,j]
                if p == [-1,-1]:
                    self.h = float('inf')
                    break
                r += w
                visited.add((p[0],p[1]))
                self.h += (SHIP_WIDTH//2 - p[1])*2
        else:
            # move the heaviest containers to the left side of the ship until the left side is within the valid range
            visited = set()
            while not self.valid_range_small < l < self.valid_range_large:
                w = 0
                p = [-1,-1]
                for i in range(SHIP_HEIGHT+SHIP_BUFF):
                    for j in range(SHIP_WIDTH//2, SHIP_WIDTH):
                        if self.ship[i][j] and l + self.ship[i][j].weight < self.valid_range_large and self.ship[i][j].weight > w and (i,j) not in visited:
                            w = self.ship[i][j].weight
                            p = [i,j]
                if p == [-1,-1]:
                    self.h = float('inf')
                    break
                l += w
                visited.add((p[0],p[1]))
                self.h += (p[1]-SHIP_WIDTH//2)*2

    # take all containers on the left and move them to the right side of the ship
    def move_containers_other_half(self, states):
        for i in range(SHIP_HEIGHT+SHIP_BUFF):
            for j in range(SHIP_WIDTH):
                if self.ship[i][j] and self.ship[i][j].name != "UNUSED":
                    pos = Position(Location.SHIP, [i,j])

                    state = copy.deepcopy(self)
                    container = state.ship[pos.m][pos.n]

                    containers_above = state.containers_above(pos)
                    prev = self.crane_position
                    while containers_above:
                        above_pos = containers_above.pop()
                        # move to the current container to move
                        if prev != above_pos:
                            (prev, cost) = state.crane_position.move_to(above_pos, state.ship if above_pos.in_ship() else state.buffer)
                            state.moves.append(Move(prev, above_pos, cost))
                            state.g += cost

                        # search for a good place to move the container
                        (move_to, cost) = state.search_from(above_pos, True, True)
                        state.swap(above_pos, move_to)
                        state.crane_position = copy.deepcopy(move_to)
                        state.moves.append(Move(above_pos, move_to, cost, state.ship[move_to.m][move_to.n]))
                        state.g += cost

                    # move to the container
                    if state.crane_position != pos:
                        (prev, cost) = state.crane_position.move_to(pos, state.ship if pos.in_ship() else state.buffer)
                        state.moves.append(Move(prev, pos, cost))
                        state.g += cost

                    # move the container to the other side of the ship
                    (search_to, cost) = state.search_from(pos, True, True, state.use_right if j < SHIP_WIDTH//2 else state.use_left)
                    state.swap(pos, search_to)
                    state.crane_position = copy.deepcopy(search_to)
                    state.moves.append(Move(pos, search_to, cost, container))
                    state.g += cost

                    state.calculate_h()

                    states.append(state)

    def use_right(self, pos):
        if pos.n < SHIP_WIDTH//2:
            return float('inf')
        return 0
    
    def use_left(self, pos):
        if pos.n >= SHIP_WIDTH//2:
            return float('inf')
        return 0

    def is_goal(self):
        return max(self.left_weight, self.right_weight)/max(1, min(self.left_weight, self.right_weight)) < 1.1 and self.crane_position.in_crane_rest() and not self.containers_in_buffers()
    
    def __eq__(self, other):
        return super().__eq__(other)
    
    def __hash__(self) -> int:
        return super().__hash__()