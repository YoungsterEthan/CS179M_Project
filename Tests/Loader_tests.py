import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from Load_Balance.Loader import Loader
from Manifest import Manifest
from ContainerData import ContainerData

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/../Manifests/"

    # def test_unload_only_easy(self):
    #     print("test_unload_only_easy(ShipCase1)")
    #     manifest = Manifest(self.path, "ShipCase1")
    #     manifest.read_manifest()
    #     loader = Loader(manifest)
    #     moves = loader.load_unload([],[
    #         ContainerData("Cat"),
    #         ])
    #     time = 0
    #     for move in moves:
    #         time += move.time_to_move
    #         print(move)
    #     print("Total time: " + str(time))

    #     assert 0 < time <= 26 # easy cases should be optimal

    # def test_load_only_easy(self):
    #     print("test_load_only_easy(ShipCase2)")
    #     manifest = Manifest(self.path, "ShipCase2")
    #     manifest.read_manifest()
    #     loader = Loader(manifest)
    #     moves = loader.load_unload([
    #         ContainerData("Bat", 431),
    #         ],[])
        
    #     time = 0
    #     for move in moves:
    #         time += move.time_to_move
    #         print(move)
    #     print("Total time: " + str(time))

    #     assert 0 < time <= 18 # easy cases should be optimal

    # def test_load_unload_easy(self):
    #     print("test_load_unload_easy(ShipCase3)")
    #     manifest = Manifest(self.path, "ShipCase3")
    #     manifest.read_manifest()
    #     loader = Loader(manifest)
    #     moves = loader.load_unload([
    #         ContainerData("Bat", 532),
    #         ContainerData("Rat", 6317),
    #         ],[
    #         ContainerData("Cow"),
    #         ])
        
    #     time = 0
    #     for move in moves:
    #         time += move.time_to_move
    #         print(move)
    #     print("Total time: " + str(time))

    #     assert 0 < time <= 46 # easy cases should be optimal

    def test_unload_shipcase3(self):
        print("test_load_unload_easy(ShipCase3)")
        manifest = Manifest(self.path, "ShipCase3")
        manifest.read_manifest()
        loader = Loader(manifest)
        moves = loader.load_unload([
            ],[
            ContainerData("Ewe"),
            ContainerData("Cat"),
            ])
        
        time = 0
        for move in moves:
            time += move.time_to_move
            print(move)
        print("Total time: " + str(time))

        assert 0 < time <= 46 # easy cases should be optimal

    # def test_load_unload_easy2(self):
    #     print("test_load_unload_easy(ShipCase4)")
    #     manifest = Manifest(self.path, "ShipCase4")
    #     manifest.read_manifest()
    #     loader = Loader(manifest)
    #     moves = loader.load_unload([
    #         ContainerData("Nat", 2543),
    #         ],[
    #         ContainerData("Doe"),
    #         ])
        
    #     time = 0
    #     for move in moves:
    #         time += move.time_to_move
    #         print(move)
    #     print("Total time: " + str(time))

    #     assert 0 < time <= 44 # easy cases should be optimal

    # def test_load_unload_easy3(self):
    #     print("test_load_unload_easy(ShipCase5)")
    #     manifest = Manifest(self.path, "ShipCase5")
    #     manifest.read_manifest()
    #     loader = Loader(manifest)
    #     moves = loader.load_unload([
    #         ContainerData("Nat", 153),
    #         ContainerData("Rat", 2321),
    #         ],[
    #         ContainerData("Hen"),
    #         ContainerData("Pig"),
    #         ])

    # hard tests commented out to reduce runtime on github actions
    
    # def test_load_unload_hard(self):
    #     print("test_load_unload_med(test_manifest)")
    #     manifest = Manifest(self.path, "test_manifest")
    #     manifest.read_manifest()
    #     loader = Loader(manifest)
    #     moves = loader.load_unload([
    #         ContainerData("Fish", "04323"),
    #         ContainerData("Cat", "04324"),
    #         ContainerData("Dog", "04325"),
    #         ContainerData("Bird", "04327"),
    #         ContainerData("Turtle", "04328"),
    #         ContainerData("Lizard", "04329"),
    #         ContainerData("Snake", "04330"),
    #         # ContainerData("Rat", "04331"),
    #         # ContainerData("Mouse", "04332"),
    #         # ContainerData("Hamster", "04333"),
    #         ],[
    #         ContainerData("Red", "00000"),
    #         ContainerData("Purple", "00000"),
    #         ContainerData("Green", "00000"),
    #         ContainerData("Red", "00000"),
    #         ])
    #     time = 0
    #     for move in moves:
    #         time += move.time_to_move
    #         print(move)
    #     print("Total time: " + str(time))

    #     assert time <= 269 # 234 is the best known time + 15% margin of error

    # def test_load_unload_full_hard(self):
    #     print("test_load_unload_full_hard(full_manifest)")
    #     manifest = Manifest(self.path, "full_manifest")
    #     manifest.read_manifest()
    #     loader = Loader(manifest)
    #     moves = loader.load_unload([
    #         ContainerData("LOAD_ME", "00001"),
    #         ContainerData("LOAD_ME", "00002"),
    #         ],[
    #         ContainerData("UNLOAD_ME", "00001"),
    #         ContainerData("UNLOAD_ME", "00002"),
    #         ])
    #     time = 0
    #     for move in moves:
    #         time += move.time_to_move
    #         print(move)
    #     print("Total time: " + str(time))

    #     assert time <= 434 # 378 is the best known time + 15% margin of error

if __name__ == "__main__":
    print("Running Loader tests")
    unittest.main()