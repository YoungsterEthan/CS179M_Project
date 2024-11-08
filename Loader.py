## The Loader class is responsible for loading and unloading containers
## Edits the manifest and saves the edited file using Manifest
## The edited manifest will be the result of completing all listed moves
class Loader:
    def __init__(self):
        self.manifest = None

    ## Given a list of containers to load and a list of containers to unload
    ## return the Moves the operator needs to perform
    ## will update the manifest
    def load_unload(self, containers_to_load, containers_to_unload):
        pass