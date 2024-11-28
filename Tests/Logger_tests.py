import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from Logger import Logger
from Manifest import Manifest
from ContainerData import ContainerData

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.logname = "testlog.txt"
        self.manifests_path = os.path.dirname(os.path.abspath(__file__)) + "\\..\\Manifests\\"

    def test_logs(self):
        os.remove(self.log.logpath + self.log.logname)
        self.log.log_comment("Comment: Hello log file")
        self.log.log_sign_in("John Smith")
        self.log.log_sign_in("Anil Patel")

        #test declaration and read
        p = Manifest(self.manifests_path, "test_manifest")
        p.log.logname = "testlog.txt"
        p.read_manifest()


        #test data at
        container = p.data_at(1,1)
        print("name: " , container.name)
        print("weight: ", container.weight)

        #test set at
        newcontainer = ContainerData("John's shrimp and stuff" , 231)
        p.set_at(1, 4, newcontainer)
        container2 = p.data_at(1,4)
        print("name: " , container2.name)
        print("weight: ", container2.weight)

        #test is NAN
        if(p.is_NAN(1, 1)):
            print("(1, 1) is NAN")
        if(p.is_NAN(1, 12)):
            print("(1, 12) is NAN")

        #test save
        p.save()

        self.log.log_close_manifest(p)

if __name__ == "__main__":
    print("Running Logger tests")
    unittest.main()