BUFF_HEIGHT = 4 # height of the buffer
BUFF_WIDTH = 24 # width of the buffer
SHIP_HEIGHT = 8 # height of the ship
SHIP_WIDTH = 12 # width of the ship
SHIP_BUFF = 2   # height of the extra space above the ship

SHIP_VIRTUAL_CELL = [SHIP_HEIGHT+SHIP_BUFF, 0]  # location of the virtual cell for the ship
BUFF_VIRTUAL_CELL = [BUFF_HEIGHT, BUFF_WIDTH-1] # location of the virtual cell for the buffer

MAX_STATES = 5000 # max number of states to keep in the heap
STATE_CULL = 100  # number of states to keep when culling the heap

EST_COST = 20 # estimated cost to move the crane from the truck to the ship and back to the truck