import os
from pathlib import Path

os.system("echo 'hello world'")

def run():
    path = Path(__file__).parent.absolute()
    pathstr = str(path)
    pathstr = pathstr + "/pwmanager.py"
    os.system("python3 " + pathstr)
