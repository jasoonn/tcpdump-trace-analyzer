from argparse import ArgumentParser
import sys
from functools import cmp_to_key
from packet import packet
import math
import matplotlib.pyplot as plt

#Process data
def parsePacket(fileName, startTime=0, endTime=10000000000000):
    inputFile = open(fileName, "r")
    data = inputFile.readlines()
    baseTime = getBaseTime(data)
    faultLineNum = []
    Packets = []
    startTime += baseTime
    endTime += baseTime
    for i, line in enumerate(data):
        tmp = packet(line)
        if tmp.process():
            if tmp.getTime()>=startTime and tmp.getTime()<endTime:
                Packets.append(tmp)
        else:
            faultLineNum.append(i+1)
    return (inputFile, faultLineNum, Packets, startTime)

#Comparator for sort list
def nonePortCompare(item1, item2):
    def compareTwoIP(IP1, IP2):
        for i in range(3):
            if int(IP1[:IP1.find('.')]) > int(IP2[:IP2.find('.')]):
                return 1
            elif int(IP1[:IP1.find('.')]) < int(IP2[:IP2.find('.')]):
                return -1
            else:
                IP1 = IP1[IP1.find('.')+1:]
                IP2 = IP2[IP2.find('.')+1:]
        if float(IP1) > float(IP2) :
            return 1
        elif float(IP1) < float(IP2):
            return -1
        return 0

    if compareTwoIP(item1[0],item2[0])!=0:
        return compareTwoIP(item1[0],item2[0])
    else:
        return compareTwoIP(item1[1],item2[1])

def portCompare(item1, item2):
    def compareTwoIP(IP1, IP2):
        for i in range(4):
            if int(IP1[:IP1.find('.')]) > int(IP2[:IP2.find('.')]):
                return 1
            elif int(IP1[:IP1.find('.')]) < int(IP2[:IP2.find('.')]):
                return -1
            else:
                IP1 = IP1[IP1.find('.')+1:]
                IP2 = IP2[IP2.find('.')+1:]
        if float(IP1) > float(IP2) :
            return 1
        elif float(IP1) < float(IP2):
            return -1
        return 0

    if compareTwoIP(item1[0],item2[0])!=0:
        return compareTwoIP(item1[0],item2[0])
    else:
        return compareTwoIP(item1[1],item2[1])

def firstCompare(item1, item2):
    if item1[0]>item2[0]:
        return 1
    elif item1[0]==item2[0]:
        return 0
    else:
        return -1

# Get the first valid packet time
def getBaseTime(data):
    for i in data:
        try:
            baseTime = parseDate(i)
            return baseTime
        except:
            continue
#Get maximum time
def getMaxTime(datas):
    max = -1
    for data in datas:
        if data[-1][0]>max:
            max = data[-1][0]    
    max = max*1.01
    return max
# Check the date is valid
def validDate(line):
    try:
        parseDate(line)
        return True
    except:
        return False

#Connect consequtive numbers together
def process_Fail(lines):
    failLine = []
    start = -1
    tick = -1
    for i in lines:
        if tick != -1:
            if i-1 != tick:
                failLine.append([start, tick])
                start = i
                tick = i
            else:
                tick = i
        else:
            start = i
            tick = i
    return failLine

#Parse args
def processCommand():
    parser = ArgumentParser()
    parser.add_argument('inputFile', help='Input filename')
    parser.add_argument('--outputFile', help='Output filename')

    parser.add_argument('--N', default=50 ,help='Filter packet according to the number')
    parser.add_argument('--port', action='store_true', default=False, help='Consider to the port level')
    parser.add_argument('--printFault', action='store_true', default=False, help='Consider to the port level')

    parser.add_argument('--subnet', help='Only consider packets belong to subnet')
    return parser.parse_args()

#Parse the date to second
def parseDate(parse):
    parse = parse[7:22]
    startHr = int(parse[0:2])
    startMin = int(parse[3:5])
    startSec = float(parse[6:15])
    return startHr*3600 + startMin*60 + startSec

#Interact with user
def interact(logArr, ths, fix):
    index = 0
    possible = []
    valid = False
    for i in logArr:
        if i[4]>int(ths):
            possible.append(i)
            print(index, i[0]+'_'+i[1], i[4])
            index += 1
    arr = []
    if fix == False:
        while (valid == False):
            valid = True
            qInput = input("Choose IP pair to show RTT and distribution(max: 7)?    e.g. 0 2 5 \n")
            try:
                arr = list(map(int, qInput.split(" ")))
            except:
                valid = False
                continue
            if len(arr)>7:
                print("Too much index")
                valid = False
                continue
            for i in arr:
                if i>index-1 or i<0:
                    print("Error index!")
                    valid = False
    else:
        arr = [8, 13, 0, 2, 3, 4]
    candidate = []
    for i in arr:
        candidate.append([possible[i][0],possible[i][1]])
    labels = []
    for i in candidate:
        labels.append(i[0] + '_' + i[1])
    return (candidate, labels)


def interactBool(sentence):
    qInput = input(sentence + "(Y/N)\n")
    if qInput == 'Y' or qInput== 'y':
        return True
    else:
        return False

if __name__ == '__main__':
    print(interactBool("hah"))
