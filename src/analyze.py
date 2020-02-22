import csv
import sys
from functools import cmp_to_key
import matplotlib.pyplot as plt 
from utils import portCompare, nonePortCompare, getBaseTime, validDate, process_Fail, processCommand, parseDate, firstCompare
from Packet import Packet
import pickle

if __name__ == '__main__':
    args = processCommand()
    print(args)
    inputFile = open(args.inputFile, "r")
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
    print(len(Packets))
    
    if args.analyzeRTT:
        print("Analyze RTT.")
        x = []
        y = []
        data = []
        possible = []
        for i, packet in enumerate(Packets):
            if (i%1000 ==0):
                print(i)
            if packet.checkIP(args.IP1, args.IP2)==False:
                continue
            if packet.getSeq() != -1:
                possible.append(packet)
            if packet.getAck() != -1:
                for j, pair in enumerate(possible):
                    if pair.getSeq() == packet.getAck():
                        if packet.getRecv(True) == pair.getSender(True) and packet.getSender(True) == pair.getRecv(True):
                            x.append(pair.getTime()-baseTime)
                            y.append(packet.getTime()-pair.getTime())
                            data.append([pair.getTime()-baseTime, packet.getTime()-pair.getTime()])
                            possible.pop(j)
                

        #Plot
        data = sorted(data, key=cmp_to_key(firstCompare))
        plt.plot([j[0] for j in data], [k[1] for k in data],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=3)
        #plt.plot(x, y,  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=3)
        if (args.IP1 != None and args.IP2 != None):
            plt.suptitle(args.IP1 + " / " + args.IP2, fontsize=16)
        plt.xlim(0,2500)
        plt.xlabel('Time (s)')
        plt.ylabel('RTT (s)') 
        plt.savefig(args.outputFile)
        plt.show()
        print(len(data))

        #Store
        if (args.storeRTT!=None):
            with open(args.storeRTT, "wb") as fp:
                pickle.dump(data, fp)
            with open("Log","a") as logFile:
                logFile.write(args.storeRTT+'\n')


    elif args.getIPPair:
        outputFile = open(args.outputFile, 'w', newline='')
        logArr = []
        #Process data
        for i, packet in enumerate(Packets):
            time = packet.getTime()
            if (i%1000 ==0):
                print(i)
            existing = False
            for pair in logArr:
                if packet.checkIP(pair[0], pair[1]):
                    pair[3] = time
                    pair[4] +=1
                    existing = True
                    break
            if existing ==False:
                sender = packet.getSender(args.port)
                recv = packet.getRecv(args.port)
                if args.subnet != None:
                    if sender.find(args.subnet)!=-1:
                        logArr.append([sender, recv, time, time, 1])
                    elif recv.find(args.subnet)!=-1:
                        logArr.append([recv, sender, time, time, 1])
                    else:
                        continue
                else:
                    logArr.append([sender, recv, time, time, 1])

        #Write output pair to csvFile
        writer = csv.writer(outputFile)
        writer.writerow(["FirstIP", "SecondIP", "First", "Second", "# recv"])
        if args.port:
            compare = portCompare
        else:
            compare = nonePortCompare
        logArr = sorted(logArr, key=cmp_to_key(compare))
        for i in logArr:
            if i[4]>int(args.N):
                writer.writerow(i)
        #Write Client Pair over number
        writer.writerow("")
        writer.writerow(["Client"])
        prev = ""
        for i in logArr:
            if i[4]>int(args.N):
                if i[0]!=prev:
                    prev = i[0]
                    writer.writerow([i[0]])
        #Write Server Pair over number
        writer.writerow("")
        writer.writerow(["Server"])
        for i in range(len(logArr)):
            tmp = logArr[i][0]
            logArr[i][0] = logArr[i][1]
            logArr[i][1] = tmp
        logArr = sorted(logArr, key=cmp_to_key(compare))
        for i in logArr:
            if i[4]>int(args.N):
                if i[0]!=prev:
                    prev = i[0]
                    writer.writerow([i[0]])
        #Write Server has over
        writer.writerow("")
        writer.writerow(["Server", "# Packets"])
        number=0
        for i in logArr:
            if prev != i[0]:
                if number>int(args.N):
                    writer.writerow([prev,number])
                number = i[4]
                prev = i[0]
            else:
                number += i[4]
        outputFile.close()
    else:
        print("Do nothing, please specify the task!")

    #Print fail number
    if args.printFault:
        for index, i in enumerate(process_Fail(faultLineNum)):
            print(index+1, i)
    inputFile.close()
