import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from RecoveryLogger import RecoveryLogger
from Move import Move
from Load_Balance.Position import Position, Location
from ContainerData import ContainerData


class TestRecoveryLogger(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/../"

    def test_create(self):
        rl = RecoveryLogger(self.path)
        rl.delete()

        rl.create([])
        
        with open(self.path + rl.recovery_file, "r") as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 2)
        self.assertEqual(int(lines[0]), 0)
        self.assertEqual(int(lines[1]), 0)

    def test_recover(self):
        rl = RecoveryLogger(self.path)
        rl.delete()

        m = Move(Position(Location.TRUCK), Position(Location.SHIP, [0, 1]), 5)

        rl.create([m])

        # generally it makes no sense to call recover after create, 
        # but for testing purposes we can do it
        rl2 = RecoveryLogger(self.path)
        
        moves, last_completed = rl2.recover()

        self.assertEqual(len(moves), 1)
        self.assertEqual(last_completed, 0)
        self.assertEqual(m, moves[0])

    def test_save_next_move(self):
        rl = RecoveryLogger(self.path)
        rl.delete()

        m1 = Move(Position(Location.CRANE_REST), Position(Location.SHIP, [0, 1]), 5)
        m2 = Move(Position(Location.SHIP, [0, 1]), Position(Location.SHIP, [0, 2]), 5, ContainerData("test", 100))

        rl.create([m1, m2])
        
        rl.save_next_move()

        with open(self.path + rl.recovery_file, "r") as f:
            lines = f.readlines()

        self.assertEqual(int(lines[0]), 2)
        self.assertEqual(int(lines[1]), 1)

        # generally it makes no sense to call recover after create, 
        # but for testing purposes we can do it
        rl2  = RecoveryLogger(self.path)
        moves, last_completed = rl2.recover()
        self.assertEqual(len(moves), 2)
        self.assertEqual(last_completed, 1)
        self.assertEqual(m1, moves[0])
        self.assertEqual(m2, moves[1])

if __name__ == "__main__":
    print("Running RevoveryLogger tests")
    unittest.main()