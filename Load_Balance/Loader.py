from consts import MAX_STATES, STATE_CULL, SHIP_HEIGHT, SHIP_WIDTH
from Load_Balance.LoadState import LoadState
from Load_Balance.Position import Position, Location
from Manifest import Manifest
from ContainerData import ContainerData
from typing import List
from collections import defaultdict
import copy
import heapq

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
        culled_states = []

        # frontier counter
        f = 0

        print("(Loader)frontier " + str(f) + " states: " + str(len(states)))

        # searching for the goal state by popping the best seen state off the heap and expanding it
        while states:
            state = heapq.heappop(states)

            # if this is a goal state we found a good solution
            if(state.is_goal()):
                self.update_manifest(state)
                return state.moves

            if not states and culled_states:
                print("(Loader)re-expanding " + str(STATE_CULL) + " states")
                for _ in range(STATE_CULL):
                    heapq.heappush(states, heapq.heappop(culled_states))
            
            n_states = state.next_states()
            if f % 100 == 0:
                print("(Loader)frontier " + str(f) + " states: " + str(len(states)) + " current best g: " + str(state.g) + " h: " + str(state.h))
            f += 1
            
            for n_state in n_states:
                heapq.heappush(states, n_state)

            # cull states to re exapand later if needed
            keep_states = []
            if len(states) > MAX_STATES:
                print("(Loader)culling " + str(len(states)-STATE_CULL) + " states")
                # save the STATE_CULL best states
                for _ in range(STATE_CULL):
                    heapq.heappush(keep_states, heapq.heappop(states))

                for s in states:
                    heapq.heappush(culled_states, s)
                
                states = keep_states

        assert False, "No solution found, fire joey8angelo"

    # a map of containers names to the set of positions they are in
    def get_unload_map(self, containers, state):
        unload_map = defaultdict(set)
        for i in range(SHIP_HEIGHT):
            for j in range(SHIP_WIDTH):
                if state.ship[i][j] and state.ship[i][j] in containers:
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
                state = copy.deepcopy(init_state)        # clone the initial state
                state.containers_to_unload = curr.copy() # fill in the containers to unload
                state.calculate_h()                      # calculate the heuristic
                heapq.heappush(states, state)            # add the state to the heap
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