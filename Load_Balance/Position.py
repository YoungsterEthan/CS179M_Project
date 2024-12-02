from consts import SHIP_HEIGHT, SHIP_WIDTH, SHIP_BUFF, BUFF_HEIGHT, BUFF_WIDTH, SHIP_VIRTUAL_CELL, BUFF_VIRTUAL_CELL
import copy
from typing import List
from ContainerData import ContainerData

class Location:
    SHIP = "SHIP"
    BUFFER = "BUFFER"
    TRUCK = "TRUCK"
    CRANE_REST = "CRANE_REST"

'''
    Position class represents a position in different locations
    centralizes the logic for moving between locations and calculating the cost of that move
'''
class Position:
    # the m,n coordinates should align with the size of the location they are in
    # for example the ship is 10x12 so the m,n coordinates should be in the range [0,0]-[9,11]
    # the 1x1 locations such as CRANE_REST and TRUCK should be in the range [0,0]x[0,0]
    def __init__(self, location: Location, mn=[0,0]):
        self.m = mn[0]
        self.n = mn[1]
        self.location = location

    def __eq__(self, value):
        return self.m == value.m and self.n == value.n and self.location == value.location
    
    def __hash__(self) -> int:
        return hash((self.m, self.n, self.location))

    # moves from the current position to the given position
    # returns the previous position and the cost of this move
    def move_to(self, pos: 'Position', loc: List[ContainerData] = None):
        old_p = copy.deepcopy(self)
        
        # move within the same location
        if self.location == pos.location:
            assert self.location == Location.SHIP or self.location == Location.BUFFER, "Invalid move, " + self.location + " is not big enough for a move"
            in_virtual = self.in_ship_virtual_cell() or self.in_buf_virtual_cell() or pos.in_ship_virtual_cell() or pos.in_buf_virtual_cell()
            if in_virtual or loc == None:
                if not in_virtual: # if either location is a virtual cell the manhattan distance actually is correct
                    print("(move_to)WARNING: No location data provided for move within the same location, assuming a manhattan distance")
                c = abs(self.m - pos.m) + abs(self.n - pos.n)
            else:
                n_p = copy.deepcopy(pos)
                c_p = copy.deepcopy(self)
                # if pos is to the left swap them
                if c_p.n > n_p.n:
                    c_p, n_p = n_p, c_p

                c = 0

                # move right
                while c_p.n != n_p.n and c_p.move_right():
                    c += 1

                    if c_p.location == Location.BUFFER:
                        t = BUFF_HEIGHT
                    else:
                        t = SHIP_HEIGHT

                    while c_p.m < t and loc[c_p.m][c_p.n].name != "UNUSED":
                        if c_p.m == n_p.m:
                            break
                        c += 1
                        c_p.move_up()
                
                # c_p and n_p are in the same horizontal position
                # move to n_p vertically
                c += abs(c_p.m - n_p.m)

        # move between ship and buffer is 4 plus manhattan distance to/from their virtual cells
        elif self.in_ship() and pos.in_buf():
            c = 4 + abs(self.m-SHIP_VIRTUAL_CELL[0]) + abs(self.n-SHIP_VIRTUAL_CELL[1]) + abs(pos.m-BUFF_VIRTUAL_CELL[0]) + abs(pos.n-BUFF_VIRTUAL_CELL[1])
        elif self.in_buf() and pos.in_ship():
            c = 4 + abs(self.m-BUFF_VIRTUAL_CELL[0]) + abs(self.n-BUFF_VIRTUAL_CELL[1]) + abs(pos.m-SHIP_VIRTUAL_CELL[0]) + abs(pos.n-SHIP_VIRTUAL_CELL[1])

        # move between the ship and truck is 2 + manhattan distance to the virtual cell
        elif self.in_ship() and pos.in_truck():
            c = 2 + abs(self.m-SHIP_VIRTUAL_CELL[0]) + abs(self.n-SHIP_VIRTUAL_CELL[1])
        elif self.in_truck() and pos.in_ship():
            c = 2 + abs(pos.m-SHIP_VIRTUAL_CELL[0]) + abs(pos.n-SHIP_VIRTUAL_CELL[1])

        # move between the buffer and truck is 2 + manhattan distance to the virtual cell
        elif self.in_buf() and pos.in_truck():
            c = 2 + abs(self.m-BUFF_VIRTUAL_CELL[0]) + abs(self.n-BUFF_VIRTUAL_CELL[1])
        elif self.in_truck() and pos.in_buf():
            c = 2 + abs(pos.m-BUFF_VIRTUAL_CELL[0]) + abs(pos.n-BUFF_VIRTUAL_CELL[1])

        # move between the crane rest and ship is 1 plus manhattan distance to the virtual cell
        elif self.in_crane_rest() and pos.in_ship():
            c = 1 + abs(pos.m-SHIP_VIRTUAL_CELL[0]) + abs(pos.n-SHIP_VIRTUAL_CELL[1])
        elif self.in_ship() and pos.in_crane_rest():
            c = 1 + abs(self.m-SHIP_VIRTUAL_CELL[0]) + abs(self.n-SHIP_VIRTUAL_CELL[1])

        # move between the crane rest and buffer is 1 plus manhattan distance to the virtual cell
        elif self.in_crane_rest() and pos.in_buf():
            c = 1 + abs(pos.m-BUFF_VIRTUAL_CELL[0]) + abs(pos.n-BUFF_VIRTUAL_CELL[1])
        elif self.in_buf() and pos.in_crane_rest():
            c = 1 + abs(self.m-BUFF_VIRTUAL_CELL[0]) + abs(self.n-BUFF_VIRTUAL_CELL[1])

        # move between the crane rest and truck is 1
        elif self.in_crane_rest() and pos.in_truck():
            c = 1
        elif self.in_truck() and pos.in_crane_rest():
            c = 1
        
        else:
            assert False, "Invalid move"

        # apply this move
        self.m = pos.m
        self.n = pos.n
        self.location = pos.location
        
        # return the prev pos and cost of this move
        return (old_p, c)

    def is_virtual_cell(self):
        return self.in_buf_virtual_cell() or self.in_ship_virtual_cell()

    def in_buf_virtual_cell(self):
        return self.m == BUFF_VIRTUAL_CELL[0] and self.n == BUFF_VIRTUAL_CELL[1] and self.location == Location.BUFFER
    
    def in_ship_virtual_cell(self):
        return self.m == SHIP_VIRTUAL_CELL[0] and self.n == SHIP_VIRTUAL_CELL[1] and self.location == Location.SHIP

    def in_buf(self):
        return self.location == Location.BUFFER
    
    def in_ship(self):
        return self.location == Location.SHIP
    
    def in_ship_buff(self):
        return self.location == Location.SHIP and self.m >= SHIP_HEIGHT

    def in_truck(self):
        return self.location == Location.TRUCK

    def in_crane_rest(self):
        return self.location == Location.CRANE_REST

    def move_right(self):
        assert self.in_ship() or self.in_buf(), "Position must be in ship or buffer"

        if self.in_buf() and self.n+1 >= BUFF_WIDTH:
            return False
        elif self.in_ship() and self.n+1 >= SHIP_WIDTH:
            return False

        self.n += 1
        return True
    
    def move_left(self):
        assert self.in_ship() or self.in_buf(), "Position must be in ship or buffer"

        if self.in_buf() and self.n <= 0:
            return False
        elif self.in_ship() and self.n <= 0:
            return False

        self.n -= 1
        return True

    def move_up(self):
        assert self.in_ship() or self.in_buf(), "Position must be in ship or buffer"

        if self.in_buf() and self.m+1 >= BUFF_HEIGHT:
            return False
        elif self.in_ship() and self.m+1 > SHIP_HEIGHT+SHIP_BUFF: # position can be 1 above the top of the ship
            return False

        self.m += 1
        return True

    def move_down(self):
        assert self.in_ship() or self.in_buf(), "Position must be in ship or buffer"

        if self.in_buf() and self.m <= 0:
            return False
        elif self.in_ship() and self.m <= 0:
            return False

        self.m -= 1
        return True
    
    def __str__(self):
        if self.location == Location.SHIP:
            return "SHIP[" + str(self.m) + ", " + str(self.n) + "]"
        elif self.location == Location.BUFFER:
            return "BUFFER[" + str(self.m) + ", " + str(self.n) + "]"
        elif self.location == Location.TRUCK:
            return "TRUCK"
        elif self.location == Location.CRANE_REST:
            return "CRANE_REST"
        elif self.location == Location.SHIP_VIRTUAL_CELL:
            return "SHIP_VIRTUAL_CELL"
        elif self.location == Location.BUFF_VIRTUAL_CELL:
            return "BUFF_VIRTUAL_CELL"
        else:
            return "INVALID"