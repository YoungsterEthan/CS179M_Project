## A RecoveryLogger is made when the operator starts making moves
## It will log last completed move and the list of all moves calculated
## When the operator completes all moves the RecoveryLogger will be deleted
class RecoveryLogger:
    ## Initialize the RecoveryLogger
    def __init__(self):
        self.recovery_file = "default_file.txt"
        self.steps = None
        self.last_completed = None

    ## Recover from the recovery file
    ## If no recovery file exists there is nothing to recover
    def recover(self):
        pass

    ## Write the last completed move to the recovery file
    def save_next_move(self):
        pass

    ## Delete the recovery file
    def delete(self):
        pass