## Logger is the interface to write out to the standard log file
class Logger:
    def __init__(self):
        self.operator = None

    ## Use the current date and time to generate the log files name
    def generate_log_filename(self):
        pass

    ## Log a move that was made by the operator
    def log_move(self, move):
        pass

    ## Log a comment that the operator wants to make
    def log_comment(self, comment):
        pass

    ## Log a sign in by the operator
    ## Updates the current operator
    def log_sign_in(self, operator):
        pass