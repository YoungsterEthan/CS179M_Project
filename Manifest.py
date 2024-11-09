import numpy as np
## Manifest is the interface for interacting with the manifest file
## The manifest file is a grid of ContainerData objects
class Manifest:
    def __init__(self, manifest_path, txtfile):
        self.manifest_path = manifest_path
        self.manifest = txtfile
        self.WeightMatrix = []
        self.ValueMatrix = []

    ## read the manifest file at manifest_path
    ## and store the data in manifest for future use
    def read_manifest(self):
        with open("./Manifests/examplemanifest.txt", 'r') as f:
            List = [line.strip() for line in f]
        
        WeightList = []
        ValueList = []

        for i in List:
            i = i[9:]
            WeightList.append(i[:7])
            ValueList.append(i[9:])
        
        WeightMatrix = []
        ValueMatrix = []

        for i in range(0, 8):
            WeightRow = WeightList[12 * i: (12 * (i + 1))]
            WeightMatrix.append(WeightRow)
            ValueRow = ValueList[12 * i: (12 * (i + 1))]
            ValueMatrix.append(ValueRow)
        
        WeightMatrix = np.array(WeightMatrix)
        ValueMatrix = np.array(ValueMatrix)

        #WeightMatrix contains all the weights
        #Value Matrix contains all the values, (container name, NAN, UNUSED)
        return WeightMatrix, ValueMatrix
        pass

    ## Determine if a position is NAN
    def is_NAN(self, x, y):
        pass

    ## Get the ContainerData at a position in the grid
    def data_at(self, x, y):

        pass

    ## Set the ContainerData at a position in the grid
    def set_at(self, x, y, container_data):
        pass

    ## Save the edited manifest data to a new file
    ## with name manifest_pathOUTBOUND.txt
    def save(self):
        OutboundList = []
        position = ""
        weight = "{00000}"
        label = "UNUSED"
        iterator = 0
        for x in range(1, 9):
            if(x < 10):
                x = "0" + str(x)
            x = str(x)
            for y in range(1, 13):
                if(y < 10):
                    y = "0" + str(y)
                y = str(y)

                position = "[" + x + ',' + y + "]"
                OutboundList.append(position + ", " + weight + ", " + label + "\n")

        with open('./Manifests/examplemanifestOUTBOUND.txt', 'w') as f:
            for i in OutboundList:
                f.write(i)
        pass

path = "./Manifests/examplemanifest.txt"
txtfile = path.replace(".txt", "")
txtfile = txtfile.replace("./Manifests/", "")

p = Manifest(path, txtfile);
p.read_manifest()
p.save()

