from subprocess import Popen, PIPE, CalledProcessError
import os
import threading

class VirtualMachine:
    serial = ""
    isRunning = False
    qemuProcess = Popen( "./vm-start.sh", stdout=PIPE, bufsize=1, universal_newlines=True    )

    def explode(self):
        self.qemuProcess.kill()
        self.isRunning = False

    def runVM(self):
        self.isRunning = True
        if self.isRunning:
            with self.qemuProcess as p:
                for line in p.stdout:
                   
                    self.serial = line.split()[4]
                    print(line.split()[4])
            if p.returncode != 0:
                raise CalledProcessError(p.returncode, p.args)


myEpicVM = VirtualMachine()
vmThread = threading.Thread(
    target=myEpicVM.runVM
   
)

