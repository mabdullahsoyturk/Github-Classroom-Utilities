import subprocess
import os
import glob

def send_to_moss():
    subprocess.run(f'./moss -l java -d spring22-lab7-*/src/*/*.java', shell=True, check=True, stderr=subprocess.PIPE).stderr.decode("utf-8")