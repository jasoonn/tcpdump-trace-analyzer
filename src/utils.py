from argparse import ArgumentParser
import sys

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
    parser.add_argument('outputFile', help='Output filename')

    parser.add_argument('--IP1', help='Consider first IP')
    parser.add_argument('--IP2', help='Consider second IP')

    parser.add_argument('--N', default=50 ,help='Filter packet according to the number')
    parser.add_argument('--port', action='store_true', default=False, help='Consider to the port level')
    parser.add_argument('--printFault', action='store_true', default=False, help='Consider to the port level')
    parser.add_argument('--storeRTT', help='Store RTT Data as this fileName')

    parser.add_argument('--subnet', help='Only consider packets belong to subnet')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--getIPPair', action='store_true', default=False, help='Choose to get IP pair')
    group.add_argument('--analyzeRTT', action='store_true', default=False, help='Choose to analyze RTT')
    return parser.parse_args()

#Parse the date to second
def parseDate(parse):
    parse = parse[7:22]
    startHr = int(parse[0:2])
    startMin = int(parse[3:5])
    startSec = float(parse[6:15])
    return startHr*3600 + startMin*60 + startSec

#Parse LOG
def parseLog(fileName):
    with open(fileName,"r")as f:
        lines = f.readlines()
        files = []
        for i in lines:
            if i.find('\n')!=-1:
                files.append(i[:-1])
            else:
                files.append(i)
        print(files)
        return files
        

if __name__ == '__main__':
    parseLog(sys.argv[1])