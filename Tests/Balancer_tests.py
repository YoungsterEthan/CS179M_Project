import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from Load_Balance.Balancer import Balancer
from Manifest import Manifest

class TestBalancer(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/../Manifests/"

    def test_balance_easy(self):
        print("test_unload_only_easy(ShipCase1)")
        manifest = Manifest(self.path, "ShipCase1")
        manifest.read_manifest()
        balancer = Balancer(manifest)
        moves = balancer.balance()
        time = 0
        for move in moves:
            time += move.time_to_move
            print(move)
        print("Total time: " + str(time))

        assert time == 34


    def test_balance_easy2(self):
        print("test_load_only_easy(ShipCase2)")
        manifest = Manifest(self.path, "ShipCase2")
        manifest.read_manifest()
        balancer = Balancer(manifest)
        moves = balancer.balance()
        time = 0
        for move in moves:
            time += move.time_to_move
            print(move)
        print("Total time: " + str(time))

        assert time == 40

    def test_balance_easy3(self):
        print("test_load_unload_easy(ShipCase3)")
        manifest = Manifest(self.path, "ShipCase3")
        manifest.read_manifest()
        balancer = Balancer(manifest)
        moves = balancer.balance()
        time = 0
        for move in moves:
            time += move.time_to_move
            print(move)
        print("Total time: " + str(time))
        
        assert time == 44

    def test_balance_easy4(self):
        print("test_load_unload_easy(ShipCase4)")
        manifest = Manifest(self.path, "ShipCase4")
        manifest.read_manifest()
        balancer = Balancer(manifest)
        moves = balancer.balance()
        time = 0
        for move in moves:
            time += move.time_to_move
            print(move)
        print("Total time: " + str(time))
        
        assert time == 60

    def test_balance_easy5(self):
        print("test_load_unload_easy(ShipCase5)")
        manifest = Manifest(self.path, "ShipCase5")
        manifest.read_manifest()
        balancer = Balancer(manifest)
        moves = balancer.balance()
        time = 0
        for move in moves:
            time += move.time_to_move
            print(move)
        print("Total time: " + str(time))

        assert time == 0

if __name__ == "__main__":
    print("Running Balancer tests")
    unittest.main()