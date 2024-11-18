import numpy as np
from ContainerData import ContainerData
## Manifest is the interface for interacting with the manifest file
## The manifest file is a grid of ContainerData objects
class Manifest:
    def __init__(self, manifest_path, txtfile):
        self.manifest_path = manifest_path
        self.manifest_name = txtfile
        self.ContainerMatrix = []

    ## read the manifest file at manifest_path
    ## and store the data in manifest for future use
    def read_manifest(self):
        with open("./Manifests/"+ self.manifest_name + ".txt", 'r') as f:
            List = [line.strip() for line in f]
        
        WeightList = []
        NameList = []

        for i in List:
            i = i[9:]
            WeightList.append(i[:7])
            NameList.append(i[9:])
        
        ContainerMatrix = []

        for i in range(0, 8):
            WeightRow = WeightList[12 * i: (12 * (i + 1))]
            NameRow = NameList[12 * i: (12 * (i + 1))]

            ContainerRow = []
            for j in range(0,12):
                c = ContainerData(NameRow[j], WeightRow[j])
                ContainerRow.append(c)
            
            ContainerMatrix.append(ContainerRow)
        
        self.ContainerMatrix = ContainerMatrix
        pass

    ## Determine if a position is NAN
    def is_NAN(self, x, y):
        if(self.ContainerMatrix[x - 1][y - 1].name == "NAN"):
            return True
        else:
            return False
        pass

    ## Get the ContainerData at a position in the grid
    def data_at(self, x, y):
        weight = self.ContainerMatrix[x - 1][y - 1].weight
        weight = weight[1:-1]

        while(weight[0] == "0"):
            weight = weight[1:]

        weight = int(weight)

        container = ContainerData(self.ContainerMatrix[x - 1][y - 1].name, weight)
        return container
        pass

    ## Set the ContainerData at a position in the grid
    def set_at(self, x, y, container_data):
        self.ContainerMatrix[x - 1][y - 1].name = container_data.name
        
        weight = str(container_data.weight)
        while(len(weight) < 5):
            weight = "0" + weight
        weight = '{' + weight + '}'

        self.ContainerMatrix[x - 1][y - 1].weight = weight
        pass

    ## Save the edited manifest data to a new file
    ## with name manifest_pathOUTBOUND.txt
    def save(self):
        OutboundList = []
        position = ""
        weight = "{00000}"
        name = "UNUSED"
        iterator = 0
        for x in range(1, 9):
            storex = x
            for y in range(1, 13):
                weight = self.ContainerMatrix[storex - 1][y - 1].weight
                name = self.ContainerMatrix[storex - 1][y - 1].name

                if(storex < 10):
                    x = "0" + str(storex)
                x = str(x)
                if(y < 10):
                    y = "0" + str(y)
                y = str(y)

                position = "[" + x + ',' + y + "]"
                OutboundList.append(position + ", " + weight + ", " + name + "\n")

        with open('./Manifests/' + self.manifest_name + 'OUTBOUND.txt', 'w') as f:
            for i in OutboundList:
                f.write(i)
        pass


path = "./Manifests/examplemanifest.txt" #change this line to input later
txtfile = path.replace(".txt", "")
txtfile = txtfile.replace("./Manifests/", "")

#test declaration and read
p = Manifest(path, txtfile);
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