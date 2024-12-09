from consts import SHIP_HEIGHT, SHIP_WIDTH, SHIP_BUFF, BUFF_HEIGHT, BUFF_WIDTH
from Load_Balance.Position import Position, Location
from ContainerData import ContainerData
from Manifest import Manifest
from Move import Move
from typing import List
import copy
import math

'''
    A unique State is:
        containers_to_load: list of ContainerData of the containers to load
        containers_to_unload: list of Positions of the containers to unload
        ship: 2D list of ContainerData representing the ship
        buffer: 2D list of ContainerData representing the buffer
        crane_position: Position of the crane
        g: cost to reach this state
        h: heuristic cost to reach the goal

    State subclasses must implement:
        calculate_h: calculate the heuristic cost of this state
        is_goal: check if the state is a goal state
        next_states: generate states that can be reached from the current state

'''
class State:
    def __init__(self, manifest: Manifest = None):
        self.crane_position = Position(Location.CRANE_REST)
        self.moves = []
        self.g = 0
        self.h = 0
        self.ship = []
        self.ship_height_map = []
        self.buffer = []
        self.buffer_height_map = []

        if manifest is not None:
            self.build(manifest)

    # build the ship and buffer representation from the manifest
    # build the ship and buffer height maps, gives quick access to the highest container in each column
    def build(self, manifest: Manifest):
        # ship is 10x12 grid, the bottom left of the ship is at (0,0)
        # the top 2 rows are the ship_buff
        self.ship = [[ContainerData() for _ in range(SHIP_WIDTH)] for _ in range(SHIP_HEIGHT+SHIP_BUFF)]
        for i in range(SHIP_HEIGHT):
            for j in range(SHIP_WIDTH):
                if not manifest.is_NAN(i+1, j+1): # if this position is not NAN
                    self.ship[i][j] = manifest.data_at(i+1, j+1)  
                else:
                    self.ship[i][j] = None
    
        # if a column has NANs reaching the top of the ship
        # then the buffer cannot be used for that column
        for i in range(SHIP_WIDTH):
            if manifest.is_NAN(SHIP_HEIGHT, i+1):
                self.ship[8][i] = None
                self.ship[9][i] = None

        # distance from the top to the highest container in each column
        self.ship_height_map = [0 for _ in range(SHIP_WIDTH)]
        for j in range(SHIP_WIDTH):
            for i in range(SHIP_HEIGHT+SHIP_BUFF-1, -1, -1):
                if self.ship[i][j] == None or self.ship[i][j].name != "UNUSED":
                    self.ship_height_map[j] = SHIP_HEIGHT+SHIP_BUFF-i-1
                    break
                if i==0:
                    self.ship_height_map[j] = SHIP_HEIGHT+SHIP_BUFF

        # build buffer
        self.buffer = [[ContainerData() for _ in range(BUFF_WIDTH)] for _ in range(BUFF_HEIGHT)]
        self.buffer_height_map = [BUFF_HEIGHT for _ in range(BUFF_WIDTH)]
    
    # given a position return a list of containers above it
    # the containers are ordered bottom to top
    def containers_above(self, pos: Position):
        containers = []
        for i in range(pos.m+1, SHIP_HEIGHT+SHIP_BUFF):
            if self.ship[i][pos.n].name != "UNUSED":
                containers.append(Position(Location.SHIP, [i, pos.n]))
        return containers
    
    # generate all possible next states by moving all reachable containers to all open positions
    # unused because this is slow
    def all_next_states(self):
        states = []
        reachable_containers = self.get_reachable_containers()
        open_positions = self.get_open_positions()
        for pos in reachable_containers:
            self.move_to_all_open_positions(pos, states, open_positions)

        return states
    
    # generate states by moving containers out of the buffers
    def clear_buffers(self, states):
        positions = self.containers_in_buffers()
        for pos in positions:
            state = copy.deepcopy(self)

            if pos.in_ship():
                container = state.ship[pos.m][pos.n]
            else:
                container = state.buffer[pos.m][pos.n]

            if self.crane_position != pos:
                # move to the container
                (prev, cost) = state.crane_position.move_to(pos, self.ship if pos.in_ship() else self.buffer)
                state.moves.append(Move(prev, state.crane_position, cost))
                state.g += cost

            # move the container from the buffer to the ship
            (move_to, cost) = state.search_from(pos, False, False, self.unloading_containers_below)
            if move_to == None:
                continue
            state.swap(pos, move_to)
            state.crane_position = copy.deepcopy(move_to)
            state.moves.append(Move(prev, move_to, cost, container))
            state.g += cost

            state.calculate_h()

            states.append(state)

    # generate a state by moving the crane back to the crane rest
    def return_crane_rest(self, states):
        state = copy.deepcopy(self)
        if not self.crane_position.in_crane_rest():
            (prev, cost) = state.crane_position.move_to(Position(Location.CRANE_REST))
            state.moves.append(Move(prev, state.crane_position, cost))
            state.g += cost

            state.calculate_h()

            states.append(state)
    
    # swap containers at pos1 and pos2
    def swap(self, pos1, pos2):
        assert (pos1.in_ship() or pos1.in_buf()) and (pos2.in_ship() or pos2.in_buf()), "Positions must be in ship or buffer, pos1: " + str(pos1) + " pos2: " + str(pos2)
        # swap containers at pos and open_pos
        if pos1.in_ship() and pos2.in_ship():
            self.ship[pos1.m][pos1.n], self.ship[pos2.m][pos2.n] = self.ship[pos2.m][pos2.n], self.ship[pos1.m][pos1.n]
            if (self.ship[pos1.m][pos1.n].name == "UNUSED") ^ (self.ship[pos2.m][pos2.n].name == "UNUSED"):
                if self.ship[pos1.m][pos1.n].name == "UNUSED":
                    self.ship_height_map[pos1.n] += 1
                    self.ship_height_map[pos2.n] -= 1
                else:
                    self.ship_height_map[pos1.n] -= 1
                    self.ship_height_map[pos2.n] += 1

        elif pos1.in_ship() and pos2.in_buf():
            self.ship[pos1.m][pos1.n], self.buffer[pos2.m][pos2.n] = self.buffer[pos2.m][pos2.n], self.ship[pos1.m][pos1.n]
            if (self.ship[pos1.m][pos1.n].name == "UNUSED") ^ (self.buffer[pos2.m][pos2.n].name == "UNUSED"):
                if self.ship[pos1.m][pos1.n].name == "UNUSED":
                    self.ship_height_map[pos1.n] += 1
                    self.buffer_height_map[pos2.n] -= 1
                else:
                    self.ship_height_map[pos1.n] -= 1
                    self.buffer_height_map[pos2.n] += 1

        elif pos1.in_buf() and pos2.in_ship():
            self.buffer[pos1.m][pos1.n], self.ship[pos2.m][pos2.n] = self.ship[pos2.m][pos2.n], self.buffer[pos1.m][pos1.n]
            if (self.buffer[pos1.m][pos1.n].name == "UNUSED") ^ (self.ship[pos2.m][pos2.n].name == "UNUSED"):
                if self.buffer[pos1.m][pos1.n].name == "UNUSED":
                    self.buffer_height_map[pos1.n] += 1
                    self.ship_height_map[pos2.n] -= 1
                else:
                    self.buffer_height_map[pos1.n] -= 1
                    self.ship_height_map[pos2.n] += 1

        else:
            self.buffer[pos1.m][pos1.n], self.buffer[pos2.m][pos2.n] = self.buffer[pos2.m][pos2.n], self.buffer[pos1.m][pos1.n]
            if (self.buffer[pos1.m][pos1.n].name == "UNUSED") ^ (self.buffer[pos2.m][pos2.n].name == "UNUSED"):
                if self.buffer[pos1.m][pos1.n].name == "UNUSED":
                    self.buffer_height_map[pos1.n] += 1
                    self.buffer_height_map[pos2.n] -= 1
                else:
                    self.buffer_height_map[pos1.n] -= 1
                    self.buffer_height_map[pos2.n] += 1
    
    def move_to_all_open_positions(self, start_pos, states, open_positions=None):
        if open_positions is None:
            open_positions = self.get_open_positions()

        for open_pos in open_positions:
            if start_pos.location == open_pos.location and start_pos.m == open_pos.m-1 and start_pos.n == open_pos.n:
                continue
            state = copy.deepcopy(self)

            if start_pos.in_ship():
                container = state.ship[start_pos.m][start_pos.n]
            else:
                container = state.buffer[start_pos.m][start_pos.n]

            # move to start pos
            if state.crane_position != start_pos:
                (prev, cost) = state.crane_position.move_to(start_pos, state.ship if start_pos.in_ship() else state.buffer)
                state.moves.append(Move(prev, start_pos, cost))
                state.g += cost
            
            # move the container from start_pos to open_pos
            state.swap(start_pos, open_pos)
            (prev, cost) = state.crane_position.move_to(open_pos, state.ship if open_pos.in_ship() else state.buffer)
            state.moves.append(Move(prev, open_pos, cost, container))
            state.g += cost
            
            state.calculate_h()
            
            states.append(state)

    def search_from(self, pos, use_buff, use_ship_buff, h_func = lambda x: 0):
        curr = copy.deepcopy(pos)
        positions = self.get_open_positions()
        best_cost = float('inf')
        best_h = float('inf')
        best_pos = None
        for p in positions:
            bad_pos = (p.m-1 == curr.m or p.m == curr.m) and p.n == curr.n and p.location == curr.location
            skip_buff = not (use_buff or p.in_ship())
            skip_ship_buff = not (use_ship_buff or (p.in_ship() and p.m < SHIP_HEIGHT))
            if bad_pos or skip_buff or skip_ship_buff:
                continue
            (curr, cost) = curr.move_to(p, self.ship if p.in_ship() else self.buffer)
            h = h_func(p)
            if cost+h < best_cost+best_h:
                best_cost = cost
                best_h = h
                best_pos = copy.deepcopy(p)

        if math.isnan(best_cost):
            print("hello")

        return (best_pos, best_cost)

    def get_reachable_containers(self):
        reachable_containers = []
        for i in range(BUFF_WIDTH):
            if self.buffer_height_map[i] < BUFF_HEIGHT and self.buffer[BUFF_HEIGHT-self.buffer_height_map[i]-1][i] and self.buffer[BUFF_HEIGHT-self.buffer_height_map[i]-1][i].name != "UNUSED":
                reachable_containers.append(Position(Location.BUFFER, [BUFF_HEIGHT-self.buffer_height_map[i]-1, i]))

        for i in range(SHIP_WIDTH):
            if self.ship_height_map[i] < SHIP_HEIGHT+SHIP_BUFF and self.ship[SHIP_HEIGHT+SHIP_BUFF-self.ship_height_map[i]-1][i] and self.ship[SHIP_HEIGHT+SHIP_BUFF-self.ship_height_map[i]-1][i].name != "UNUSED":
                reachable_containers.append(Position(Location.SHIP, [SHIP_HEIGHT+SHIP_BUFF-self.ship_height_map[i]-1, i]))

        return reachable_containers
    
    def containers_in_buffers(self):
        reachable = self.get_reachable_containers()
        positions = []
        for pos in reachable:
            if pos.in_buf():
                positions.append(pos)
            if pos.in_ship_buf() and self.ship[pos.m][pos.n]:
                positions.append(pos)

        return positions
    
    def get_open_positions(self):
        open_positions = []
        for i in range(BUFF_WIDTH):
            if self.buffer_height_map[i] > 0:
                open_positions.append(Position(Location.BUFFER, [BUFF_HEIGHT-self.buffer_height_map[i], i]))
        
        for i in range(SHIP_WIDTH):
            if self.ship_height_map[i] > 0:
                open_positions.append(Position(Location.SHIP, [SHIP_HEIGHT+SHIP_BUFF-self.ship_height_map[i], i]))
        
        return open_positions


    # comparison for heapq
    def __lt__(self, other):
        return self.g + self.h < other.g + other.h
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        for i in range(SHIP_HEIGHT+SHIP_BUFF):
            for j in range(SHIP_WIDTH):
                if self.ship[i][j] != other.ship[i][j]:
                    return False
                
        for i in range(BUFF_HEIGHT):
            for j in range(BUFF_WIDTH):
                if self.buffer[i][j] != other.buffer[i][j]:
                    return False
                
        self.crane_position == other.crane_position
                
        return True
    
    def __hash__(self) -> int:
        return hash(tuple([tuple(row) for row in self.ship]) + tuple([tuple(row) for row in self.buffer]) + (self.crane_position.m, self.crane_position.n))