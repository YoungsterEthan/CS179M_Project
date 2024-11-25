from consts import SHIP_HEIGHT, SHIP_WIDTH, SHIP_BUFF, BUFF_HEIGHT, BUFF_WIDTH, SHIP_VIRTUAL_CELL, BUFF_VIRTUAL_CELL
import copy

class Location:
    SHIP = "ship"
    BUFFER = "buffer"
    TRUCK = "truck"
    CRANE_REST = "crane_rest"


class Position:
    # the m,n coordinates should align with the size of the location they are in
    # for example the ship is 10x12 so the m,n coordinates should be in the range [0,0]-[9,11]
    # the 1x1 locations such as CRANE_REST and TRUCK should be in the range [0,0]x[0,0]
    def __init__(self, location, mn=[0,0]):
        self.m = mn[0]
        self.n = mn[1]
        self.location = location

    # def __eq__(self, value):
    #     return self.m == value.m and self.n == value.n and self.location == value.location

    # moves from the current position to the given position
    # returns the previous position and the cost of this move
    def move_to(self, pos):
        # move within the same location is manhattan distance TODO: this assumes the locations are not blocked by some obstacle like a wall of containers blocking the path
        if self.location == pos.location:
            c = abs(self.m-pos.m) + abs(self.n-pos.n)

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

        old_p = copy.deepcopy(self)

        # apply this move
        self.m = pos.m
        self.n = pos.n
        self.location = pos.location
        
        # return the cost of this move
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