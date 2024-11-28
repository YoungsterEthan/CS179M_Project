from Load_Balance.State import State
from Load_Balance.Position import Position, Location
from Move import Move
from ContainerData import ContainerData
from consts import SHIP_VIRTUAL_CELL, BUFF_VIRTUAL_CELL, EST_COST
import copy

'''
    State subclass for Loading/unloading
    goal state is when there are no containers to load or unload
    next_states generates all possible states that can be reached from the current state
        states are generated by 
            loading the top container in the list of containers to load
            unloading each container in the list of containers to unload
            removing each container out of the buffer
            removing each container out of the buffer zone in the ship
    the heuristic of a state is 
        manhattan distance of each container to unload
        distance to load any container
        distance to move each container out of the buffer
        distance to move each container out of the buffer zone in the ship
'''
class LoadState(State):
    def __init__(self, containers_to_load=[], containers_to_unload=[], manifest=None):
        self.containers_to_load = containers_to_load
        self.containers_to_unload = containers_to_unload
        super().__init__(manifest)
    
    # calculate the heuristic cost of this state
    def calculate_h(self):
        self.h = 0
        # manhattan distance of each container to unload
        for pos in self.containers_to_unload:
            self.h += abs(pos.m-SHIP_VIRTUAL_CELL[0]) + abs(pos.n-SHIP_VIRTUAL_CELL[1])*2

        # distance to load somewhere in the ship
        for pos in self.containers_to_load:
            self.h += self.search(Position(Location.SHIP, SHIP_VIRTUAL_CELL), False, False, self.unloading_containers_below)[1]*2

        # distance to move somewhere else in the ship
        for pos in self.containers_in_ship_buff:
            self.h += self.search(pos, False, False, self.unloading_containers_below)[1]*2

        # distance to move somewhere in the ship plus distance to buffer virtual cell
        for pos in self.containers_in_buff:
            self.h += self.search(Position(Location.SHIP, SHIP_VIRTUAL_CELL), False, False, self.unloading_containers_below)[1]*2
            self.h += abs(pos.m-BUFF_VIRTUAL_CELL[0]) + abs(pos.n-BUFF_VIRTUAL_CELL[1])

    
    # check if the state is a goal state
    # if there are no containers to load or unload
    # and if there are no containers in the buffer or ship buffer zone
    def is_goal(self):
        return not self.containers_to_load and not self.containers_to_unload and not self.containers_in_buff and not self.containers_in_ship_buff
    
    # generate a list of states that can be reached from the current state
    def next_states(self):
        states = []

        pruned =  self.next_unloading_states(states)
        pruned += self.next_loading_state(states)
        pruned += self.next_remove_buffer_states(states)
        pruned += self.next_remove_ship_buffer_states(states)

        return (states, pruned)

    
    # build a state for each container to unload
    def next_unloading_states(self, states):
        pruned = 0
        for i in range(len(self.containers_to_unload)):
            state = copy.deepcopy(self) # copy the current state
            state.containers_to_unload = state.containers_to_unload[:i] + state.containers_to_unload[i+1:] # remove the current container to unload from this state
            cost = state.unload(self.containers_to_unload[i]) # unload the container
            if cost != float('inf'): # this state is pruned
                state.g += cost # update the cost of unloading
                state.calculate_h() # calculate the heuristic cost of this state
                states.append(state)
            else:
                pruned += 1

        return pruned
    
    # build a state for loading a container
    def next_loading_state(self, states):
        pruned = 0
        if self.containers_to_load:
            state = copy.deepcopy(self)
            cost = state.load(state.containers_to_load.pop())
            if cost != float('inf'): # if the ship is full a load will fail
                state.g += cost
                state.calculate_h()
                states.append(state)
            else:
                pruned += 1
        return pruned

    # load a container into the ship
    def load(self, container):
        cost = 0
        old_pos = copy.deepcopy(self.crane_position)
        from_p = old_pos

        if not self.crane_position.in_truck():
            # move to truck
            (prev, ct) = self.crane_position.move_to(Position(Location.TRUCK))
            cost += ct
            self.moves.append(Move(prev, Position(Location.TRUCK), ct))
            from_p = copy.deepcopy(self.crane_position)

        # move to virtual cell
        (_, cs) = self.crane_position.move_to(Position(Location.SHIP, SHIP_VIRTUAL_CELL))
        cost += cs

        # find place to drop container, use the unloading_containers_below function to estimate the future cost
        (_, cd) = self.search_swap(self.crane_position, False, False, self.unloading_containers_below, container)
        cost += cd
        self.moves.append(Move(from_p, copy.deepcopy(self.crane_position), cd+cs, container))
        
        if cost == float('inf'): # load failed, pruned this state
            return float('inf')

        return cost
    
    # unload a container from the ship
    def unload(self, pos):
        cost = 0
        start_pos = copy.deepcopy(self.crane_position)
        
        if not pos.in_ship():
            # move to virtual cell
            (_, cs) = self.crane_position.move_to(Position(Location.SHIP, SHIP_VIRTUAL_CELL))
            cost += cs

        containers_to_move = self.containers_above(pos)
        while containers_to_move:
            container = containers_to_move.pop()
            
            # if there is a container to unload in the way then prune this state
            # we should move the container on top first before the current one
            if self.contains_eq_pos(self.containers_to_unload, container):
                return float('inf')
            
            # move to container
            (prev, cm) = self.crane_position.move_to(container, self.ship)
            cost += cm
            if (start_pos if start_pos else prev) != container:
                self.moves.append(Move(start_pos if start_pos else prev, container, cm))
            start_pos = None
            
            # move container elsewhere, use the unloading_containers_below function to estimate the future cost
            (prev, cd) = self.search_swap(self.crane_position, True, True, self.unloading_containers_below)
            cost += cd
            if self.crane_position.location == Location.SHIP:
                self.moves.append(Move(prev, copy.deepcopy(self.crane_position), cd, self.ship[self.crane_position.m][self.crane_position.n]))
            else:
                self.moves.append(Move(prev, copy.deepcopy(self.crane_position), cd, self.buffer[self.crane_position.m][self.crane_position.n]))

        # move crane to pos
        (prev, cu) = self.crane_position.move_to(pos, self.ship)
        cost += cu
        if prev != pos:
            self.moves.append(Move(prev, pos, cu))

        # unload container
        # an 'unload container' will never be located in the ship buffer or buffer
        # this is because the only time a container can move to these locations is in the containers_to_move while loop,
        # and this loop will terminate if it tries to move a container in the containers_to_unload list before the current container
        container = self.ship[self.crane_position.m][self.crane_position.n]
        self.ship[self.crane_position.m][self.crane_position.n] = ContainerData()
        self.ship_height_map[self.crane_position.n] += 1
        (prev, cf) = self.crane_position.move_to(Position(Location.TRUCK))
        cost += cf
        self.moves.append(Move(prev, Position(Location.TRUCK), cf, container))

        return cost
    
    # count the number of containers that need to be unloaded below the given position
    # times the estimated cost to unload a container
    def unloading_containers_below(self, pos):
        count = 0
        curr_pos = copy.deepcopy(pos)
        while curr_pos.move_down():
            if self.contains_eq_pos(self.containers_to_unload, curr_pos):
                count += EST_COST
        return count