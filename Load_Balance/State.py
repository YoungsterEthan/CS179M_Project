from Load_Balance.Position import Position, Location
from ContainerData import ContainerData
from consts import SHIP_HEIGHT, SHIP_WIDTH, SHIP_BUFF, BUFF_HEIGHT, BUFF_WIDTH, SHIP_VIRTUAL_CELL, BUFF_VIRTUAL_CELL
import copy
from typing import List
from Manifest import Manifest
from Move import Move

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
        next_states: generate a list of states that can be reached from the current state

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

        # track the Positions of containers in the buffer and ship buff
        self.containers_in_buff = []
        self.containers_in_ship_buff = []

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
    
    # given a list of containers return the first position in the list that has the given name
    def contains_name(self, containers: List[ContainerData], name: str):
        for i,container in enumerate(containers):
            if container.name == name:
                return i
        return -1
    
    # given a list of positions and a position return true 
    # if the list contains a position with the same m,n coordinates
    def contains_eq_pos(self, containers_pos: List[Position], pos: Position):
        for i in containers_pos:
            if i.m == pos.m and i.n == pos.n and i.location == pos.location:
                return True
        return False

    # The distance the container would move if it were to be dropped at the current pos
    def drop_container_at(self, pos: Position, use_ship_buff: bool):
        assert pos.in_ship() or pos.in_buf(), "Position must be in ship or buffer"

        d = 0
        if pos.in_buf():
            d = self.buffer_height_map[pos.n]-(BUFF_HEIGHT-pos.m) # distance to drop from above the buffer minus the distance from the top of the buffer to the current position
        else:
            d = self.ship_height_map[pos.n]-(SHIP_HEIGHT+SHIP_BUFF-pos.m) # distance to drop from above the ship minus the distance from the top of the ship to the current position

        # if the container drops a negative distance then it is not possible to drop the container at this position
        if d < 0:
            return float('inf')
        
        # container can not be dropped above the ship or buffer
        if d == 0 and (pos.m == BUFF_HEIGHT if pos.in_buf() else pos.m == SHIP_HEIGHT+SHIP_BUFF):
            return float('inf')
        
        # if we cannot use the ships buffer and the calculated end position is in the ship buffer
        if not use_ship_buff and pos.m-d >= SHIP_HEIGHT:
            return float('inf')
        
        return d
    
    # given a position return a list of containers above it
    # the containers are ordered bottom to top
    def containers_above(self, pos: Position):
        containers = []
        for i in range(pos.m+1, SHIP_HEIGHT+SHIP_BUFF):
            if self.ship[i][pos.n].name != "UNUSED":
                containers.append(Position(Location.SHIP, [i, pos.n]))
        return containers

    # find the best position to place a container given the starting position 
    # and swap the container at the starting position with the container at the best position
    # can toggle between considering the buffer or not, useful for loading as we dont want to load into the buffer
    # define search_h to give a heuristic cost of placing a container at a given position, unique to each subclass
    # if given a container do not swap and simply set the container at the best position
    def search_swap(self, start_position: Position, use_buffer: bool, use_ship_buffer: bool, search_h = lambda _: 0, container: ContainerData = None):
        assert not (start_position.in_buf() and use_buffer), "Cannot start in buffer and use buffer"
        # if start_position == Position(Location.SHIP, [2,1]) and self.ship[1][0].name != "UNUSED":
        #     print("hello")

        R = self.R_search(start_position, use_ship_buffer, search_h) # search on the right
        L = self.L_search(start_position, use_buffer, use_ship_buffer, search_h) # search on the left

        p = R[0] if R[1] < L[1] else L[0] # choose the best position
        c = R[1] if R[1] < L[1] else L[1] # cost of moving to the best position
        if c == float('inf'): # if the cost is infinite then we cannot place the container at this position
            return (start_position, c)

        self.crane_position = p # move the crane to the best position

        # if the position we moved container to in the ship buf or buf add it to respective lists
        if self.crane_position.in_ship_buff():
            self.containers_in_ship_buff.append(copy.deepcopy(self.crane_position))
        elif self.crane_position.in_buf():
            self.containers_in_buff.append(copy.deepcopy(self.crane_position))

        # if we are not swapping then set container
        if container:
            self.ship[p.m][p.n] = container
            self.ship_height_map[p.n] -= 1
            return (start_position, c)
        
        # else swap the containers
        if start_position.in_ship() and p.in_ship():  # swap in ship
            self.ship[start_position.m][start_position.n], self.ship[p.m][p.n] = self.ship[p.m][p.n], self.ship[start_position.m][start_position.n]
            self.ship_height_map[start_position.n] += 1
            self.ship_height_map[p.n] -= 1
        elif start_position.in_ship() and p.in_buf(): # swap from ship to buffer
            self.ship[start_position.m][start_position.n], self.buffer[p.m][p.n] = self.buffer[p.m][p.n], self.ship[start_position.m][start_position.n]
            self.ship_height_map[start_position.n] += 1
            self.buffer_height_map[p.n] -= 1
        elif start_position.in_buf() and p.in_ship(): # swap from buffer to ship
            self.buffer[start_position.m][start_position.n], self.ship[p.m][p.n] = self.ship[p.m][p.n], self.buffer[start_position.m][start_position.n]
            self.buffer_height_map[start_position.n] += 1
            self.ship_height_map[p.n] -= 1
        else:                                         # swap in buffer
            self.buffer[start_position.m][start_position.n], self.buffer[p.m][p.n] = self.buffer[p.m][p.n], self.buffer[start_position.m][start_position.n]
            self.buffer_height_map[start_position.n] += 1
            self.buffer_height_map[p.n] -= 1

        return (start_position, c)
    
    # find the best position to place a container given the starting position
    def search(self, start_position: Position, use_buffer: bool, use_ship_buffer: bool, search_h = lambda _: 0):
        assert not (start_position.in_buf() and use_buffer), "Cannot start in buffer and use buffer"
        
        R = self.R_search(start_position, use_ship_buffer, search_h) # search on the right
        L = self.L_search(start_position, use_buffer, use_ship_buffer, search_h) # search on the left
        
        p = R[0] if R[1] < L[1] else L[0] # choose the best position
        c = R[1] if R[1] < L[1] else L[1] # cost of moving to the best position

        return (p, c)

    # search to the right of the given position to find the best place to drop a container
    # is inclusive of the starting position
    # define search_h to give a heuristic cost of placing a container at a given position
    def R_search(self, start_position: Position, use_ship_buffer: bool, search_h):
        curr_pos = copy.deepcopy(start_position)

        best_cost = float('inf')
        best_h = float('inf')
        best_pos = None
        
        dist = 0
        while(True):
            drop_dist = self.drop_container_at(curr_pos, use_ship_buffer) # cost of dropping the container at this position
            h = search_h(curr_pos) # heuristic cost of placing this container here
            is_not_start = (start_position.m != curr_pos.m-drop_dist or start_position.n != curr_pos.n or start_position.location != curr_pos.location)
            if is_not_start and dist+drop_dist+h < best_cost+best_h: # update best when we are not at the start position and the cost is less than the best cost
                best_cost = dist+drop_dist
                best_h = h
                best_pos = copy.deepcopy(curr_pos)
                best_pos.m -= drop_dist

            on_edge = not curr_pos.move_right()

            # hit the right edge of the ship or its not possible to get a better cost
            if (curr_pos.in_ship() and on_edge) or dist > best_cost+best_h:
                break

            if on_edge:
                (_,c) = curr_pos.move_to(Position(Location.SHIP, SHIP_VIRTUAL_CELL))
                dist += c
                continue

            dist += 1

            blocked = False
            if curr_pos.in_buf():
                blocked = curr_pos.m < BUFF_HEIGHT and (not self.buffer[curr_pos.m][curr_pos.n] or self.buffer[curr_pos.m][curr_pos.n].name != "UNUSED") # position at buff_width or there is a container in the way
            else:
                blocked = curr_pos.m < SHIP_HEIGHT+SHIP_BUFF and (not self.ship[curr_pos.m][curr_pos.n] or self.ship[curr_pos.m][curr_pos.n].name != "UNUSED") # container in the way, position at ship_width already checked

            if blocked:
                while blocked:
                    curr_pos.move_up()
                    dist += 1
                    if curr_pos.in_buf():
                        blocked = curr_pos.m < BUFF_HEIGHT and (not self.buffer[curr_pos.m][curr_pos.n] or self.buffer[curr_pos.m][curr_pos.n].name != "UNUSED")
                    else:
                        blocked = curr_pos.m < SHIP_HEIGHT+SHIP_BUFF and (not self.ship[curr_pos.m][curr_pos.n] or self.ship[curr_pos.m][curr_pos.n].name != "UNUSED")

                drop_dist = self.drop_container_at(curr_pos, use_ship_buffer)
                h = search_h(curr_pos)
                is_not_start = (start_position.m != curr_pos.m-drop_dist or start_position.n != curr_pos.n or start_position.location != curr_pos.location)
                if is_not_start and dist+drop_dist+h < best_cost+best_h:
                    best_cost = dist
                    best_h = h
                    best_pos = copy.deepcopy(curr_pos)

        return (best_pos, best_cost)
    
    # search to the left of the given position to find the best place to drop a container
    # is not inclusive of the starting position
    # define search_h to give a heuristic cost of placing a container at a given position
    def L_search(self, start_position: Position, use_buffer: bool, use_ship_buffer: bool, search_h):
        curr_pos = copy.deepcopy(start_position)

        best_cost = float('inf')
        best_h = float('inf')
        best_pos = None
        
        dist = 0
        h=0
        while(True):
            on_edge = not curr_pos.move_left()

            # hit the left edge of the buffer or its not possible to get a better cost
            if (curr_pos.in_buf() and on_edge) or dist+h > best_cost+best_h:
                break

            if on_edge:
                if use_buffer:
                    (_,c) = curr_pos.move_to(Position(Location.BUFFER, BUFF_VIRTUAL_CELL))
                    dist += c-1
                else:
                    break

            dist += 1

            if curr_pos.in_ship():
                blocked = curr_pos.m < SHIP_HEIGHT+SHIP_BUFF and (not self.ship[curr_pos.m][curr_pos.n] or self.ship[curr_pos.m][curr_pos.n].name != "UNUSED")
            else:
                blocked = curr_pos.m < BUFF_HEIGHT and (not self.buffer[curr_pos.m][curr_pos.n] or self.buffer[curr_pos.m][curr_pos.n].name != "UNUSED")

            if blocked:
                while blocked:
                    curr_pos.move_up()
                    dist += 1
                    if curr_pos.in_ship():
                        blocked = curr_pos.m < SHIP_HEIGHT+SHIP_BUFF and (not self.ship[curr_pos.m][curr_pos.n] or self.ship[curr_pos.m][curr_pos.n].name != "UNUSED")
                    else:
                        blocked = curr_pos.m < BUFF_HEIGHT and (not self.buffer[curr_pos.m][curr_pos.n] or self.buffer[curr_pos.m][curr_pos.n].name != "UNUSED")

                drop_dist = self.drop_container_at(curr_pos, use_ship_buffer)
                h = search_h(curr_pos)
                is_not_start = (start_position.m != curr_pos.m-drop_dist or start_position.n != curr_pos.n or start_position.location != curr_pos.location)
                if is_not_start and dist+drop_dist+h < best_cost+best_h:
                    best_cost = dist
                    best_h = h
                    best_pos = copy.deepcopy(curr_pos)

                continue

            drop_dist = self.drop_container_at(curr_pos, use_ship_buffer) # cost of dropping the container at this position
            h = search_h(curr_pos) # heuristic cost of placing this container here
            is_not_start = (start_position.m != curr_pos.m-drop_dist or start_position.n != curr_pos.n or start_position.location != curr_pos.location)
            if is_not_start and dist+drop_dist+h < best_cost+best_h: # update best when we are not at the start position and the cost is less than the best cost
                best_cost = dist+drop_dist
                best_h = h
                best_pos = copy.deepcopy(curr_pos)
                best_pos.m -= drop_dist

        return (best_pos, best_cost)
    
    def next_remove_buffer_states(self, states):
        pruned = 0
        while self.containers_in_buff:
            pos = self.containers_in_buff.pop()
            state = copy.deepcopy(self)
            container = state.buffer[pos.m][pos.n]
            state.buffer[pos.m][pos.n] = ContainerData()
            
            # move to this container
            (prev, cs) = state.crane_position.move_to(Position(Location.BUFFER, pos))
            state.moves.append(Move(prev, Position(Location.BUFFER, [pos.m, pos.n]), cs, container))
            state.g += cs

            # move to the ship
            (prev, cm) = state.crane_position.move_to(Position(Location.SHIP, SHIP_VIRTUAL_CELL))
            state.g += cm
            
            # drop container
            (_, cd) = state.search_swap(state.crane_position, False, False, state.unloading_containers_below, container)
            state.g += cd

            # save move from buffer to ship position
            state.moves.append(Move(prev, Position(Location.SHIP, [state.crane_position.m, state.crane_position.n]), cm+cd, container))
            
            # if we cant drop the container then prune this state
            if cd == float('inf'):
                pruned += 1
                continue

            states.append(state)

        return pruned

    def next_remove_ship_buffer_states(self, states):
        pruned = 0
        for i in range(len(self.containers_in_ship_buff)):
            state = copy.deepcopy(self)
            state.containers_in_ship_buff = state.containers_in_ship_buff[:i] + state.containers_in_ship_buff[i+1:]
            pos = self.containers_in_ship_buff[i]
            container = state.ship[pos.m][pos.n]
            state.ship[pos.m][pos.n] = ContainerData()

            if len(self.containers_above(pos)) > 0:
                pruned += 1
                continue
            
            # move to this container
            (prev, cs) = state.crane_position.move_to(Position(Location.SHIP, [pos.m, pos.n]), self.ship)
            state.moves.append(Move(prev, Position(Location.SHIP, [pos.m, pos.n]), cs))
            state.g += cs
            
            # drop container
            (prev, cd) = state.search_swap(state.crane_position, False, False, state.unloading_containers_below, container)
            state.g += cd

            # save move from buffer to ship position
            state.moves.append(Move(prev, Position(Location.SHIP, [state.crane_position.m, state.crane_position.n]), cd, container))
            
            # if we cant drop the container then prune this state
            if cd == float('inf'):
                pruned += 1
                continue

            states.append(state)

        return pruned


    # comparison for heapq
    def __lt__(self, other):
        return self.g + self.h < other.g + other.h