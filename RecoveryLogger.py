from Move import Move
from Load_Balance.Position import Position
from ContainerData import ContainerData
import os

## A RecoveryLogger is made when the operator starts making moves
## It will log last completed move and the list of all moves calculated
## When the operator completes all moves the RecoveryLogger will be deleted
## format of the file is:
## number of Moves, N
## last completed Move
## Move 1..N
class RecoveryLogger:
    ## Initialize the RecoveryLogger
    def __init__(self, recovery_path):
        self.recovery_file = "recover.txt"
        self.recovery_path = recovery_path
        self.lines = None
        self.last_task = ""

    def fexists(self):
        exists = False
        try:
            with open(self.recovery_path + self.recovery_file, "r") as _:
                exists = True
        except FileNotFoundError:
            pass

        return exists

    ## Write a new recovery file using a list of Moves
    def create(self, moves):
        exists = self.fexists()

    
        assert not exists, "create() should not be called if a recovery file already exists"
        assert self.lines == None, "create() and recover() should not be called in the same instance of RecoveryLogger"

        with open(self.recovery_path + self.recovery_file, "w") as f:
            f.write(str(len(moves)) + "\n")
            self.lines = [str(len(moves)) + "\n"]
            f.write(str(0) + "\n")
            self.lines.append(str(0) + "\n")
            f.write(self.last_task)
            self.lines.append(self.last_task + '\n')
            for i in range(len(moves)):
                f.write(self.stringify_move(moves[i]) + "\n")
                self.lines.append(self.stringify_move(moves[i]) + "\n")

    ## Convert a Move to a string
    def stringify_move(self, move):
        return move.m_from.location + " " + str(move.m_from.m) + " " + str(move.m_from.n) + " " + move.m_to.location + " " + str(move.m_to.m) + " " + str(move.m_to.n) + " " + str(move.time_to_move) + " " + str(move.container.weight) + " " + move.container.name

    ## Recover the list of Moves and the current Move from the recovery file
    ## If no recovery file exists there is nothing to recover
    def recover(self):
        exists = self.fexists()

        assert self.lines == None, "create() and recover() should not be called in the same instance of RecoveryLogger"

        if not exists:
            return None, None

        with open(self.recovery_path + self.recovery_file, "r") as f:
            self.lines = f.readlines()
        
        n_steps = int(self.lines[0])
        last_completed = int(self.lines[1])
        self.last_task = self.lines[2]
        moves = []
        for i in range(n_steps):
            moves.append(self.parse_move(self.lines[i+3]))

        return moves, last_completed
    

    ## Moves formmated as:
    ## from_location from_row from_column to_location to_row to_column time_to_move container_weight container_name
    ## rows and columns are 0 indexed
    def parse_move(self, line):
      parts = line.split()
      m_from = Position(parts[0], [int(parts[1]), int(parts[2])])
      m_to = Position(parts[3], [int(parts[4]), int(parts[5])])
      ttm = int(parts[6])
      weight = int(parts[7])
      name = parts[8]
      for i in range(9, len(parts)-1):
          name += " " + parts[i]
      container = ContainerData(name, weight)
      return Move(m_from, m_to, ttm, container)

    ## Write the last completed move to the recovery file
    def save_next_move(self):
        exists = self.fexists()
        if not exists:
            return
        with open(self.recovery_path  + self.recovery_file, "w") as f:
            f.write(self.lines[0])
            print(self.lines[1])
            self.lines[1] = str(int(self.lines[1])+1)
            f.write(self.lines[1] + "\n")
            f.write(self.last_task)
            for i in range(len(self.lines)-3):
                f.write(self.lines[i+3])

    ## Delete the recovery file
    def delete(self):
        exists = self.fexists()
        if not exists:
            return
        os.remove(self.recovery_path + self.recovery_file)
        self.lines = None