## Logger is the interface to write out to the standard log file
from datetime import datetime, timezone, timedelta
from ContainerData import ContainerData

def get_time():
    pst = timezone(timedelta(hours=-8))
    now = datetime.now(pst)
    return now.strftime("%Y-%m-%d %H:%M") + " "

class Logger:
    def __init__(self):
        self.operator = None
        pst = timezone(timedelta(hours=-8))
        now = datetime.now(pst)
        self.logname = "KeoghsPort" + str(now.strftime("%Y")) +  ".txt"
        self.currentoperator = ""

    ## Log a move that was made by the operator
    #move = 1 or 2
    #1 = onload
    #2 = unload
    #3 = moved within ship
    def log_move(self, container, move):
        with open(self.logname, 'a') as f:
            if(move == 1):
                f.write(get_time() +"\"" + container.name + "\"" +  " is onloaded\n")
            elif(move == 2):
                f.write(get_time() +"\"" + container.name + "\"" +  " is offloaded\n")
            elif(move == 3):
                f.write(get_time() +"\"" + container.name + "\"" +  " is moved within the ship\n")
        pass

    def log_open_manifest(self, manifest):
        with open(self.logname, 'a') as f:
            f.write(get_time() + "Manifest "+ manifest.manifest_name + ".txt is opened, there are "+ str(manifest.container_amount()) + " containers on the ship\n")
        pass

    def log_close_manifest(self, manifest):
        with open(self.logname, 'a') as f:
            f.write(get_time() + "Finishes a cycle. Manifest " + manifest.manifest_name + "OUTBOUND.txt was written to desktop, and a reminder pop-up to operator to send file was displayed\n")

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
