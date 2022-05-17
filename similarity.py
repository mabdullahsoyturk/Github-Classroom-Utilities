import subprocess

def send_to_moss():
    result = subprocess.run(f'./moss -l java -d spring22-lab7-*/src/*/*.java', shell=True, check=True, stdout=subprocess.PIPE).stdout.decode(utf-8)

    link = result.split("\n")[-1]

    return link
