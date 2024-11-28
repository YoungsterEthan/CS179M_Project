from ContainerData import ContainerData
from Logger import Logger
## Manifest is the interface for interacting with the manifest file
## The manifest file is a grid of ContainerData objects
class Manifest:
    def __init__(self, manifest_path, txtfile):
        self.manifest_path = manifest_path
        self.manifest_name = txtfile
        self.ContainerMatrix = []
        self.log = Logger()

    ## read the manifest file at manifest_path
    ## and store the data in manifest for future use
    def read_manifest(self):
        with open(self.manifest_path + self.manifest_name + ".txt", 'r') as f:
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
        self.log.log_open_manifest(self)

    ## Determine if a position is NAN
    def is_NAN(self, x, y):
        if(self.ContainerMatrix[x - 1][y - 1].name == "NAN"):
            return True
        else:
            return False

    ## Get the ContainerData at a position in the grid
    def data_at(self, x, y):
        weight = self.ContainerMatrix[x - 1][y - 1].weight
        weight = weight[1:-1]

        weight = int(weight)

        container = ContainerData(self.ContainerMatrix[x - 1][y - 1].name, weight)
        return container

    ## Set the ContainerData at a position in the grid
    def set_at(self, x, y, container_data):
        self.ContainerMatrix[x - 1][y - 1].name = container_data.name
        
        weight = str(container_data.weight)
        while(len(weight) < 5):
            weight = "0" + weight
        weight = '{' + weight + '}'

        self.ContainerMatrix[x - 1][y - 1].weight = weight
    
    def container_amount(self):
        sum = 0
        for containerrow in self.ContainerMatrix:
            for container in containerrow:
                if(container.name != "UNUSED" and container.name != "NAN"):
                    sum += 1
        return sum


    ## Save the edited manifest data to a new file
    ## with name manifest_pathOUTBOUND.txt
    def save(self):
        OutboundList = []
        position = ""
        weight = "{00000}"
        name = "UNUSED"
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

        with open(self.manifest_path + self.manifest_name + 'OUTBOUND.txt', 'w') as f:
            for i in OutboundList:
                f.write(i)
        self.log.log_close_manifest(self)