## Logger is the interface to write out to the standard log file
from datetime import datetime, timezone, timedelta

def get_time():
    pst = timezone(timedelta(hours=-8))
    now = datetime.now(pst)
    return now.strftime("%Y-%m-%d %H:%M") + " "

#print(get_time())

class Logger:
    def __init__(self):
        self.operator = None
        pst = timezone(timedelta(hours=-8))
        now = datetime.now(pst)
        self.logname = "KeoghsPort" + str(now.strftime("%Y")) +  ".txt"
        self.currentoperator = ""

    ## Log a move that was made by the operator
    #move = [container_name, 1 or 2]
    #1 = onload
    #2 = unload

    def log_move(self, move):
        with open(self.logname, 'a') as f:
            f.write(get_time() + "\n")
        pass

    def log_open_manifest(self, manifest):
        with open(self.logname, 'a') as f:
            f.write(get_time() + "\n")
        pass

    ## Log a comment that the operator wants to make
    def log_comment(self, comment):
        with open(self.logname, 'a') as f:
            f.write(get_time() + comment + "\n")
        pass

    ## Log a sign in by the operator
    ## Updates the current operator
    def log_sign_in(self, operator):
        with open(self.logname, 'a') as f:
            if(self.currentoperator != ""):
                f.write(get_time() + self.currentoperator + " signs out\n")
            f.write(get_time() + operator + " signs in\n")
            self.currentoperator = operator
        pass

Log = Logger()
Log.log_move("move")
Log.log_comment("I smell smoke ong")
Log.log_sign_in("John Smith")
Log.log_sign_in("Anil Patel")