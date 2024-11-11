import numpy as np
## Manifest is the interface for interacting with the manifest file
## The manifest file is a grid of ContainerData objects
class Manifest:
    def __init__(self, manifest_path, txtfile):
        self.manifest_path = manifest_path
        self.manifest_name = txtfile
        self.WeightMatrix = []
        self.ValueMatrix = []

    ## read the manifest file at manifest_path
    ## and store the data in manifest for future use
    def read_manifest(self):
        with open("./Manifests/"+ self.manifest_name + ".txt", 'r') as f:
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
        
        WeightMatrix = np.array(WeightMatrix, dtype='object')
        ValueMatrix = np.array(ValueMatrix, dtype='object')

        self.WeightMatrix = WeightMatrix
        self.ValueMatrix = ValueMatrix
        #WeightMatrix contains all the weights
        #Value Matrix contains all the values, (container name, NAN, UNUSED)
        return WeightMatrix, ValueMatrix
        pass

    ## Determine if a position is NAN
    def is_NAN(self, x, y):
        if(ValueMatrix[x - 1, y - 1] == "NAN"):
            return True
        else:
            return False
        pass

    ## Get the ContainerData at a position in the grid
    def data_at(self, x, y):
        weight = self.WeightMatrix[x - 1, y - 1]
        weight = weight[1:-1]

        while(weight[0] == "0"):
            weight = weight[1:]

        weight = int(weight)

        return (self.ValueMatrix[x - 1, y - 1], weight)
        pass

    ## Set the ContainerData at a position in the grid
    def set_at(self, x, y, container_data):
        self.ValueMatrix[x - 1, y - 1] = container_data[0]
        
        weight = str(container_data[1])
        while(len(weight) < 5):
            weight = "0" + weight
        weight = '{' + weight + '}'

        self.WeightMatrix[x - 1, y - 1] = weight
        pass

    ## Save the edited manifest data to a new file
    ## with name manifest_pathOUTBOUND.txt
    def save(self):
        OutboundList = []
        position = ""
        weight = "{00000}"
        value = "UNUSED"
        iterator = 0
        for x in range(1, 9):
            storex = x
            for y in range(1, 13):
                weight = self.WeightMatrix[storex - 1][y - 1]
                value = self.ValueMatrix[storex - 1][y - 1]

                if(storex < 10):
                    x = "0" + str(storex)
                x = str(x)
                if(y < 10):
                    y = "0" + str(y)
                y = str(y)

                position = "[" + x + ',' + y + "]"
                OutboundList.append(position + ", " + weight + ", " + value + "\n")

        with open('./Manifests/' + self.manifest_name + 'OUTBOUND.txt', 'w') as f:
            for i in OutboundList:
                f.write(i)
        pass


path = "./Manifests/examplemanifest.txt" #change this line to input later
txtfile = path.replace(".txt", "")
txtfile = txtfile.replace("./Manifests/", "")

p = Manifest(path, txtfile);
p.read_manifest()

#print(p.WeightMatrix)
#print(p.ValueMatrix)

value, weight = p.data_at(1,1)
print("value: " , value)
print("weight: ", weight)

newcontainer = ["John's shrimp and stuff" , 231]
p.set_at(1, 4, newcontainer)
value, weight = p.data_at(1,4)
print("value: " , value)
print("weight: ", weight)

p.save()