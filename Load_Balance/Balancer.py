import heapq
from Load_Balance.BalanceState import BalanceState
from consts import MAX_STATES, STATE_CULL, SHIP_HEIGHT
from Manifest import Manifest

## Balancer will balance the containers in the manifest
## Edits the manifest and saves the edited file using Manifest
## The edited manifest will be the result of completing all listed moves
class Balancer:
    def __init__(self, manifest: Manifest):
        self.manifest = manifest

    ## Given a list of containers to load and a list of containers to unload
    ## return the Moves the operator needs to perform
    ## will update the manifest
    def balance(self):
        states = [BalanceState(self.manifest)]
        states[0].calculate_h()
        
        if states[0].h == float('inf'):
            print("(Balancer)This ship cannot be balanced")
            return []
        
        culled_states = []
        visited = set()
        visited.add(states[0])

        # frontier counter
        f = 0

        print("(Balancer)frontier " + str(f) + " states: " + str(len(states)))

        # searching for the goal state by popping the best seen state off the heap and expanding it
        while states:
            state = heapq.heappop(states)

            # if this is a goal state we found a good solution
            if(state.is_goal()):
                self.update_manifest(state)
                return state.moves

            if not states and culled_states:
                print("(Balancer)re-expanding " + str(STATE_CULL) + " states")
                for _ in range(STATE_CULL):
                    heapq.heappush(states, heapq.heappop(culled_states))
            
            n_states = state.next_states()
            if f % 100 == 0:
                print("(Balancer)frontier " + str(f) + " states: " + str(len(states)) + " current best g: " + str(state.g) + " h: " + str(state.h))
            f += 1
            
            for n_state in n_states:
                if n_state not in visited:
                    visited.add(n_state)
                    heapq.heappush(states, n_state)

            # cull states to re exapand later if needed
            keep_states = []
            if len(states) > MAX_STATES:
                print("(Balancer)culling " + str(len(states)-STATE_CULL) + " states")
                # save the STATE_CULL best states
                for _ in range(STATE_CULL):
                    heapq.heappush(keep_states, heapq.heappop(states))

                for s in states:
                    heapq.heappush(culled_states, s)
                
                states = keep_states

        assert False, "No solution found, fire joey8angelo"
    
    def update_manifest(self, state):
        for i,row in enumerate(state.ship):
            if i >= SHIP_HEIGHT:
                break
            for j,container in enumerate(row):
                if container:
                    self.manifest.set_at(i+1, j+1, container)

        self.manifest.save()