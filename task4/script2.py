import sys
import re
from prefect import task, flow

@task
def get_percent(line):
    t = line.split(" ")[4][1:][:-1]
    return float(t)

@task
def ok_or_not(percent):
    if percent < 90:
        print("Not OK")
    else:
        print("OK")

@flow
def parse():
    f = open(sys.argv[1], "r")
    lines = f.readlines()
    for line in lines:
        if re.match("[0-9]+ \+ [0-9]+ mapped", line.strip()):
            percent = get_percent(line)
            ok_or_not(percent)

def main():
    parse()

		
    

if __name__ == "__main__":
    main()