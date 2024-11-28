import heapq
from Load_Balance.LoadState import LoadState
from consts import MAX_STATES, STATE_CULL, SHIP_HEIGHT, SHIP_WIDTH, SHIP_VIRTUAL_CELL, EST_COST
import copy
from collections import defaultdict
from Load_Balance.Position import Position, Location
from Manifest import Manifest
from ContainerData import ContainerData
from typing import List
from Move import Move

## The Loader class is responsible for loading and unloading containers
## Edits the manifest and saves the edited file using Manifest
## The edited manifest will be the result of completing all listed moves
class Loader:
    def __init__(self, manifest: Manifest):
        self.manifest = manifest

    ## Given a list of containers to load and a list of containers to unload
    ## return the Moves the operator needs to perform
    ## will update the manifest
    def load_unload(self, containers_to_load: List[ContainerData], containers_to_unload: List[ContainerData]):
        states = self.make_starting_states(containers_to_load, containers_to_unload) # heap of states to search

        # informational data
        p_size = len(states)
        f = 0
        pruned = 0

        print("frontier " + str(f) + " states: " + str(len(states)))

        # searching for the goal state by popping the best seen state off the heap and expanding it
        while states:
            state = heapq.heappop(states)
            
            p_size-=1
            if not p_size:
                f+=1
                print("frontier " + str(f) + " states: " + str(len(states)) + " current best cost: " + str(state.g) + " pruned: " + str(pruned))
                p_size = len(states)
                pruned = 0
            
            # if this is a goal state we found a good solution
            # with the current hueristic this is may not be optimal
            if(state.is_goal()):
                self.update_manifest(state)
                return state.moves
            
            (n_states, p) = state.next_states()
            pruned += p
            
            for n_state in n_states:
                heapq.heappush(states, n_state)

            # fail safe, if a pathological input blows up the heap cull some states
            n_states.clear()
            if len(states) > MAX_STATES:
                print("culling " + str(len(states)-STATE_CULL) + " states")
                for _ in range(STATE_CULL):
                    heapq.heappush(n_states, heapq.heappop(states))

                states = n_states

        print("(Loader)WARNING: No solution found")
        return []

    # a map of containers names to the set of positions they are in
    def get_unload_map(self, containers, state):
        unload_map = defaultdict(set)
        for i in range(SHIP_HEIGHT):
            for j in range(SHIP_WIDTH):
                if state.ship[i][j] and state.contains_name(containers, state.ship[i][j].name) != -1:
                    unload_map[state.ship[i][j].name].add(Position(Location.SHIP, [i, j]))
        return unload_map

    # When there are multiple instances of the same container in the ship decide which ones 
    # to unload by permuting all possible combinations of the containers and searching from there
    def make_starting_states(self, containers_to_load, containers_to_unload):
        # build a state from the manifest
        init_state = LoadState(containers_to_load, [], self.manifest)

        unload_map = self.get_unload_map(containers_to_unload, init_state)

        states = []

        # permute each combination of containers with the same name but different positions
        def permute(containers_to_unload, curr):
            nonlocal states, containers_to_load, unload_map
            # if we have used up all containers in the list we use the current combination we made
            if not containers_to_unload:
                state = copy.deepcopy(init_state) # clone the initial state
                state.containers_to_unload = curr.copy() # fill in the containers to unload
                heapq.heappush(states, state) # add the state to the heap
                return
            
            container = containers_to_unload.pop()
            for pos in unload_map[container.name]:
                unload_map[container.name].remove(pos)
                curr.append(pos)
                permute(containers_to_unload, curr)
                curr.pop()
                unload_map[container.name].add(pos)

            containers_to_unload.append(container)

        permute(containers_to_unload, [])

        return states
    
    def update_manifest(self, state):
        for i,row in enumerate(state.ship):
            if i >= SHIP_HEIGHT:
                break
            for j,container in enumerate(row):
                if container:
                    self.manifest.set_at(i+1, j+1, container)

        self.manifest.save()

        # final crane move to rest pos
        (p, c) = state.crane_position.move_to(Position(Location.CRANE_REST))
        state.g += c
        state.moves.append(Move(p, state.crane_position, c))