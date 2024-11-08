## Manifest is the interface for interacting with the manifest file
## The manifest file is a grid of ContainerData objects
class Manifest:
    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        self.manifest = None

    ## read the manifest file at manifest_path
    ## and store the data in manifest for future use
    def read_manifest(self):
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
        pass