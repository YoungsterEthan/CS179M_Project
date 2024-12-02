from consts import SHIP_WIDTH
import heapq
from Load_Balance.BalanceState import BalanceState
## Balancer will balance the containers in the manifest
## Edits the manifest and saves the edited file using Manifest
## The edited manifest will be the result of completing all listed moves
class Balancer:
    def __init__(self):
        self.manifest = None

    ## Balance the containers in the manifest
    ## Returns the Moves the operator needs to perform
    def balance(self):
        states = BalanceState(self.manifest)

        p_size = 1
        f = 0
        pruned = 0

        print("frontier " + str(f) + " states: " + str(len(states)))

        while states:
            state = heapq.heappop(states)

            p_size-=1
            if not p_size:
                f+=1
                print("frontier " + str(f) + " states: " + str(len(states)) + " current best cost: " + str(state.g) + " pruned: " + str(pruned))
                p_size = len(states)
                pruned = 0

            if(state.is_goal()):
                self.update_manifest(state)
                return state.moves
            
            (n_states, p) = state.next_states()
            pruned += p

            for n_state in n_states:
                heapq.heappush(states, n_state)

            n_states.clear()
            if len(states) > MAX_STATES:
                print("culling " + str(len(states)-STATE_CULL) + " states")
                for _ in range(STATE_CULL):
                    heapq.heappush(n_states, heapq.heappop(states))

                states = n_states

        print("(Balancer)WARNING: No solution found")
        return []