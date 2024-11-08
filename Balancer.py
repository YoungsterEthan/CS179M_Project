## Balancer will balance the containers in the manifest
## Edits the manifest and saves the edited file using Manifest
## The edited manifest will be the result of completing all listed moves
class Balancer:
    def __init__(self):
        self.manifest = None

    ## Balance the containers in the manifest
    ## Returns the Moves the operator needs to perform
    def balance(self):
        pass