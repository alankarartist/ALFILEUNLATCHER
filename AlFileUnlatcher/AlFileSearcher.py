import os
import re
import platform
systemName = platform.system()
if systemName == 'Windows':
    import win32api
elif systemName == 'Darwin':
    import subprocess
import sys

class AlFileSearcher():

    def __init__(self, fileName):
        super().__init__()
        self.findFileInAllDrives(fileName)

    def findFile(self, rootFolder, rex):
        for root, _, files in os.walk(rootFolder):
            for f in files:
                result = rex.search(f)
                if result:
                    print(os.path.join(root, f))

    def findFileInAllDrives(self, fileName):
        rex = re.compile(fileName)
        if systemName == 'Windows':
            for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
                self.findFile(drive, rex)
        elif systemName == 'Darwin':
            process = subprocess.Popen(['df -h | awk \'{print $NF}\''],
                                       stdout=subprocess.PIPE, shell=True)
            out, _ = process.communicate()
            out = out.splitlines()
            drives = [i.decode(encoding='utf-8', errors='strict')
                      for i in out]
            for drive in drives:
                self.findFile(drive, rex)

                
if __name__ == '__main__':
    AlFileSearcher(sys.argv[1])