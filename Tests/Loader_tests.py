import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from Load_Balance.Loader import Loader
from Manifest import Manifest
from ContainerData import ContainerData

class TestLoader(unittest.TestCase):
    def test_load(self):
        manifest = Manifest("")
        loader = Loader(manifest)
        moves = loader.load_unload([
            ContainerData("Fish", "00152"),
            ContainerData("Cat", "04324"),
            ContainerData("Dog", "04325"),
            ContainerData("Bird", "04327"),
            ContainerData("Turtle", "04328"),
            ContainerData("Lizard", "04329"),
            ContainerData("Snake", "04330"),
            ContainerData("Rat", "04331"),
            ContainerData("Mouse", "04332"),
            ContainerData("Hamster", "04333"),
            ],[
            ContainerData("Red", "04334"),
            ContainerData("Purple", "04336"),
            ContainerData("Green", "04338"),
            ContainerData("Red", "04340"),
            ])
        time = 0
        for move in moves:
            time += move.time_to_move
            print(move)
        print("Total time: " + str(time))

if __name__ == "__main__":
    print("Running Loader tests")
    unittest.main()