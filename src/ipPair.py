import csv
from functools import cmp_to_key
from Packet import Packet
from utils import portCompare, nonePortCompare

class ipPair():
    def __init__(self, packets, outputFileName, subnet, port, ths):
        self.logArr = []
        self.port = port
        self.ths = ths
        self.outputFileName = outputFileName
        #Process data
        for i, packet in enumerate(packets):
            time = packet.getTime()
            if (i%200 ==0):
                print([i, len(self.logArr)], end="\r", flush=True)
            existing = False
            for pair in self.logArr:
                if packet.checkIP(pair[0], pair[1]):
                    pair[3] = time
                    pair[4] +=1
                    existing = True
                    break
            if existing ==False:
                sender = packet.getSender(self.port)
                recv = packet.getRecv(self.port)
                if subnet != None:
                    if sender.find(subnet)!=-1:
                        self.logArr.append([sender, recv, time, time, 1])
                    elif recv.find(subnet)!=-1:
                        self.logArr.append([recv, sender, time, time, 1])
                    else:
                        continue
                else:
                    self.logArr.append([sender, recv, time, time, 1])

    def getLogArr(self):
        return self.logArr
        
    
    def close(self):
        if (self.outputFileName!=None):
            outputFile = open(self.outputFileName, 'w', newline='')
            writer = csv.writer(outputFile)
            writer.writerow(["FirstIP", "SecondIP", "First", "Second", "# recv"])
            if self.port:
                compare = portCompare
            else:
                compare = nonePortCompare
            self.logArr = sorted(self.logArr, key=cmp_to_key(compare))

            for i in self.logArr:
                if i[4]>int(self.ths):
                    writer.writerow(i)

            #Write Client Pair over number
            writer.writerow("")
            writer.writerow(["Client"])
            prev = ""
            buffer = 0
            for i in self.logArr:
                if i[0]!= prev:
                    if buffer>int(self.ths):
                        writer.writerow([prev])
                    prev = i[0]
                    buffer = i[4]
                else:
                    buffer += i[4]
            #Write Server Pair over number
            writer.writerow("")
            writer.writerow(["Server"])
            for i in range(len(self.logArr)):
                tmp = self.logArr[i][0]
                self.logArr[i][0] = self.logArr[i][1]
                self.logArr[i][1] = tmp
            self.logArr = sorted(self.logArr, key=cmp_to_key(compare))
            for i in self.logArr:
                if i[0]!= prev:
                    if buffer>int(self.ths):
                        writer.writerow([prev])
                    prev = i[0]
                    buffer = i[4]
                else:
                    buffer += i[4]
            outputFile.close()
