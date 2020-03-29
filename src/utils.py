from argparse import ArgumentParser
import sys
from functools import cmp_to_key
from Packet import Packet
import math
import matplotlib.pyplot as plt

#Process data
def parsePacket(fileName):
    inputFile = open(fileName, "r")
    data = inputFile.readlines()
    baseTime = getBaseTime(data)
    faultLineNum = []
    Packets = []
    for i, line in enumerate(data):
        tmp = Packet(line)
        if tmp.process():
            Packets.append(tmp)
        else:
            faultLineNum.append(i+1)
    return (inputFile, faultLineNum, Packets, baseTime)

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
def interact(logArr, ths):
    index = 0
    possible = []
    valid = False
    for i in logArr:
        if i[4]>int(ths):
            possible.append(i)
            print(index, i[0]+'_'+i[1], i[4])
            index += 1
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

def plotInterArrival(packets, desiredArr, outputFile):
    maxInter = 0
    upInterList = []
    downInterList = []
    upPrevTime = -1
    downPrevTime = -1
    for IPPair in desiredArr:
        for i, packet in enumerate(packets):
            if (i%200 ==0):
                print([IPPair ,i], end="\r", flush=True)
            if packet.checkIP(IPPair[0], IPPair[1])==False:
                continue
            if packet.getSender(True).find(IPPair[0]) == 0:
                if upPrevTime != -1:
                    upInterList.append(packet.getTime()-upPrevTime)
                    upPrevTime = packet.getTime()
                else:
                    upPrevTime = packet.getTime()
            else:
                if downPrevTime != -1:
                    downInterList.append(packet.getTime()-downPrevTime)
                    downPrevTime = packet.getTime()
                else:
                    downPrevTime = packet.getTime()
        maxInter = max([max(upInterList), max(downInterList)])
        print("")
        print(maxInter)
        lim = min([maxInter, 20])
        print(lim)
        
        uploadInterArr = []
        downloadInterArr = []
        for i in [x*0.001 for x in range(int(math.ceil(lim)*1000))]:
            uploadInterArr.append([i, 0])
            downloadInterArr.append([i, 0])
        for up in upInterList:
            if up < lim:
                uploadInterArr[math.floor(up*1000)][1] += 1
        for down in downInterList:
            if down < lim:
                downloadInterArr[math.floor(down*1000)][1] += 1

        # for i in uploadInterArr:
        #     print(i)

        for i in range(math.ceil(lim)*1000-1):
            uploadInterArr[i+1][1] += uploadInterArr[i][1]
            downloadInterArr[i+1][1] += downloadInterArr[i][1]


        # for i in downInterList:
        #     print(i)

        plt.plot([j[0] for j in uploadInterArr], [k[1]/len(upInterList) for k in uploadInterArr],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Uoload arrival time CDF")
        plt.plot([j[0] for j in downloadInterArr], [k[1]/len(downInterList) for k in downloadInterArr],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Download arrival time CDF")
        plt.xlabel('Inter-arrival Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(outputFile + "_" + IPPair[0] + "_" + IPPair[1] + "_interTime" + ".png") 
        plt.show()
                

        




if __name__ == '__main__':
    print(interactBool("hah"))