from packet import packet
import matplotlib.pyplot as plt
from utils import getMaxTime
import math

class rtt:
    def __init__(self, packets, baseTime, desiredArr, outputFile, colors, labels, longTime = 100, startTime=0):
        self.baseTime = baseTime
        self.desiredArr = desiredArr
        self.colors = colors
        self.labels = labels
        self.outputFile = outputFile
        self.longTime = longTime
        self.startTime = startTime
        self.packets = packets
        self.clientsRTT = []
        self.serverRTT = []
        self.overallRTT = []
        self.noRTT = False
        self.serverIP = ""
        print("Initialize RTT")

    def plotTimeSeries(self, startTime, endTime, bin=0):
        if len(self.clientsRTT) == 0 and self.noRTT == False:
            self.processClientsRTT()
            if  len(self.clientsRTT) == 0:
                self.noRTT = True

        if bin!= 0:
            for index, data in enumerate(self.clientsRTT):
                times = []
                for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
                for i in data:
                    if(startTime<=i[0] and i[0]<endTime):
                        times[math.floor((i[0]-startTime)/bin)].append(i[1])
                effectiveTime = []
                for i, packets in enumerate(times):
                    if len(packets)!=0:
                        effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                plt.scatter([j[0] for j in effectiveTime], [j[1] for j in effectiveTime], s=4, color=self.colors[index], label=self.labels[index])
            plt.legend()
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.xlabel('Time (s)')
            plt.ylabel('RTT (s)')
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeRTTScatter.png")
            plt.show()

            for index, data in enumerate(self.clientsRTT):
                times = []
                for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
                for i in data:
                    if(startTime<=i[0] and i[0]<endTime):
                        times[math.floor((i[0]-startTime)/bin)].append(i[1])
                effectiveTime = []
                for i, packets in enumerate(times):
                    if len(packets)!=0:
                        effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                plt.plot([j[0] for j in effectiveTime], [j[1] for j in effectiveTime], linewidth = 1, color=self.colors[index], label=self.labels[index])
            plt.legend()
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.xlabel('Time (s)')
            plt.ylabel('RTT (s)')
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeRTT.png")
            plt.show()
        else :            
            for index, data in enumerate(self.clientsRTT):
                plt.scatter([j[0] for j in data], [k[1]
                                                for k in data], s=2, color=self.colors[index], label=self.labels[index])
            plt.legend()
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.xlabel('Time (s)')
            plt.ylabel('RTT (s)')
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_RTT.png")
            plt.show()

    def processSpecificPairs(self, IPpairData):
        effectNum = 0
        allData = []
        for pairData in IPpairData:
            possible = []
            thisData = []
            for i, packet in enumerate(self.packets):
                if (i % 200 == 0):
                    print([pairData[0], i], end="\r", flush=True)
                if packet.checkIP(pairData[0][0], pairData[0][1]) == False or (packet.getTime()-self.baseTime) < pairData[1] or (packet.getTime()-self.baseTime) > pairData[2]:
                    continue
                possible.append(packet)
                for j, pair in enumerate(reversed(possible)):
                    if pair.getSeq() == packet.getAck():
                        if packet.getRecv(True) == pair.getSender(True) and packet.getSender(True) == pair.getRecv(True):
                            allData.append(packet.getTime()-pair.getTime())
                            thisData.append(packet.getTime()-pair.getTime())
                            possible.pop(len(possible)-j-1)
                            effectNum += 1
                            break
            print("")
            thisfilterData = []
            for i in thisData:
                if i<180:
                    thisfilterData.append(i)
            print("avg:", sum(thisfilterData)/len(thisfilterData))

        filterData = []
        for i in allData:
            if i<180:
                filterData.append(i)
        print("Total Average RTT", sum(filterData)/len(filterData))
        print("Effective Total Data:", effectNum, "after filter", len(filterData))
        print("")
        maxx = 50
        RTTAcc = []
        for i in [x*0.001 for x in range(int(maxx *1000))]:
            RTTAcc.append([i, 0])
        for i in allData:
            if i > maxx:
                continue
            RTTAcc[int(i*1000)][1] += 1

        for i in range(int(maxx*1000)-1):
            RTTAcc[i+1][1] += RTTAcc[i][1]

        for i in range(int(maxx*1000)):
            RTTAcc[i][1] /= len(filterData)

        return RTTAcc
        

    def processServer(self, serverIP, store = False):
        possible = []
        data = []
        for i, packet in enumerate(self.packets):
            if (i % 200 == 0):
                print([serverIP, i], end="\r", flush=True)
            if packet.checkIP(serverIP) == False:
                continue
            possible.append(packet)
            for j, pair in enumerate(reversed(possible)):
                if pair.getSeq() == packet.getAck():
                    if packet.getRecv(True) == pair.getSender(True) and packet.getSender(True) == pair.getRecv(True):
                        data.append([pair.getTime()-self.baseTime, packet.getTime()-pair.getTime()])
                        possible.pop(len(possible)-j-1)
                        break
        print('')
        plt.scatter([j[0] for j in data], [k[1] for k in data], s=2, color='green', label='RTT')
        plt.xlabel('Time (s)')
        plt.ylabel('RTT (s)')
        if store:
            plt.savefig(self.outputFile + "RTT" + serverIP + ".png")
        plt.show()
        self.serverRTT = data
        largeData = []
        count = 10
        for i in data:
            if len(largeData)<count:
                largeData.append(i[1])
                largeData.sort()
            else:
                if largeData[0]<i[1]:
                    largeData[0] = i[1]
                    largeData.sort()
        print("Max:", largeData)
        print("Overall Pair Number:", len(data))
        time = 0
        for i in data:
            time += i[1]
        print("Unfilter:", time/len(data))
        b = [10, 30, 50, 100, 150, 180, 200]
        for j in b:
            filterTime = 0
            filterCount = 0
            for i in data:
                diff = i[1]
                if diff>j:
                    filterCount += 1
                else:
                    filterTime += diff
            print(j, "Filter:", filterTime/(len(data)-filterCount), "filter count", filterCount)

        

    def plotServerDistribution(self, serverIP):
        if self.serverIP != serverIP:
            self.processServer(serverIP)
            self.serverIP = serverIP

        effectDataNum = 0
        over = []
        accumulated = []
        for i in [x*0.001 for x in range(int(int(self.longTime)*1000))]:
            accumulated.append([i, 0])
        for i in self.serverRTT:
            if i[0] >= int(self.startTime):
                if i[1] > int(self.longTime):
                    over.append(i[1])
                    continue
                accumulated[int(i[1]*1000)][1] += 1
                effectDataNum += 1

        for i in range(int(int(self.longTime)*1000)):
            accumulated[i][1] /= effectDataNum

        for i in range(int(int(self.longTime)*1000)-1):
            accumulated[i+1][1] += accumulated[i][1]

        print("Effective Data:",effectDataNum)
        plt.scatter([j[0] for j in accumulated], [k[1] for k in accumulated], s=2, color='green')
        plt.xlabel('Time (s)')
        plt.ylabel('RTT (s)')
        plt.savefig(self.outputFile + "_RTTCDF" + serverIP + ".png") 
        plt.show()

        plt.xscale('log')
        plt.scatter([j[0] for j in accumulated], [k[1] for k in accumulated], s=2, color='green')
        plt.xlim(0.001, 100)
        plt.xlabel('Time (s)')
        plt.ylabel('RTT (s)')
        plt.savefig(self.outputFile + "_RTTCDFxlog" + serverIP + ".png") 
        plt.show()

    def plotRTTDistribution(self):
        if len(self.clientsRTT) == 0 and self.noRTT == False:
            self.processClientsRTT()
            if  len(self.clientsRTT) == 0:
                self.noRTT = True
        # Second, plot PDF
        allOver = []
        allAccumulated = []
        for index, data in enumerate(self.clientsRTT):
            effectDataNum = 0
            over = []
            accumulated = []
            for i in [x*0.001 for x in range(int(int(self.longTime)*1000))]:
                accumulated.append([i, 0])
            for i in data:
                if i[0] >= int(self.startTime):
                    if i[1] > int(self.longTime):
                        over.append(i[1])
                        continue
                    accumulated[int(i[1]*1000)][1] += 1
                    effectDataNum += 1
            for i in range(len(accumulated)):
                accumulated[i][1] /= effectDataNum
            allAccumulated.append(accumulated)
            allOver.append(over)

        for index, data in enumerate(self.clientsRTT):
            for i in range(len(allAccumulated[index])-1):
                allAccumulated[index][i+1][1] += allAccumulated[index][i][1]
            plt.scatter([j[0]+0.0001 for j in allAccumulated[index]], [k[1]
                                                                    for k in allAccumulated[index]], s=1, color=self.colors[index], label=self.labels[index])
        plt.legend()
        plt.xlabel('RTT Time (s)')
        plt.ylabel('CDF')
        plt.savefig(self.outputFile + "rttAllCDF.png")
        plt.show()

        plt.xscale('log')
        for index, data in enumerate(self.clientsRTT):
            plt.scatter([j[0]+0.0001 for j in allAccumulated[index]], [k[1]
                                                                    for k in allAccumulated[index]], s=1, color=self.colors[index], label=self.labels[index])
        plt.legend()
        plt.xlabel('RTT Time (s)')
        plt.ylabel('CDF')
        plt.xlim(0.001, 100)
        plt.ylim(0.001, 1)
        plt.savefig(self.outputFile + "rttAllCDFxlog.png")
        plt.show()

    def processClientsRTT(self):
        #Caculate different time
        effectNum = 0
        for IPPair in self.desiredArr:
            possible = []
            data = []
            for i, packet in enumerate(self.packets):
                if (i % 200 == 0):
                    print([IPPair, i], end="\r", flush=True)
                if packet.checkIP(IPPair[0], IPPair[1]) == False:
                    continue
                possible.append(packet)
                for j, pair in enumerate(reversed(possible)):
                    if packet.getAck() == pair.getSeq() or packet.getSeq() == pair.getAck():
                        if packet.getRecv(True) == pair.getSender(True) and packet.getSender(True) == pair.getRecv(True):
                            data.append([pair.getTime()-self.baseTime,
                                        packet.getTime()-pair.getTime()])
                            possible.pop(len(possible)-j-1)
                            effectNum += 1
                            break
            self.clientsRTT.append(data)
        print("")
        print("Effective Total Data:", effectNum)
        self.maxTime = getMaxTime(self.clientsRTT)

    def getServerTimeSeries(self, startTime, endTime, serverIP, bin=0):
        if bin!=0:
            if self.serverIP != serverIP:
                self.processServer(serverIP)
                self.serverIP = serverIP
            times = []
            for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
            for i in self.serverRTT:
                if(startTime<=i[0] and i[0]<endTime):
                    times[math.floor((i[0]-startTime)/bin)].append(i[1])
            effectiveTime = []
            for i, packets in enumerate(times):
                if len(packets)!=0:
                    effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                else:
                    effectiveTime.append([startTime+i*bin, 0])
            plt.scatter([j[0] for j in effectiveTime], [j[1] for j in effectiveTime], s=4, color='green')
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('RTT (s)')
            plt.show()

            return effectiveTime
        

    def getOverallTimeSeries(self, startTime, endTime, bin=0):
        if bin!=0:
            possible = []
            data = []
            for i, packet in enumerate(self.packets):
                if (i % 200 == 0):
                    print(i, end="\r", flush=True)
                possible.append(packet)
                for j, pair in enumerate(reversed(possible)):
                    if pair.getSeq() == packet.getAck():
                        if packet.getRecv(True) == pair.getSender(True) and packet.getSender(True) == pair.getRecv(True):
                            data.append([pair.getTime()-self.baseTime, packet.getTime()-pair.getTime()])
                            possible.pop(len(possible)-j-1)
                            break
            plt.scatter([j[0] for j in data], [k[1] for k in data], s=2, color='green', label='RTT')
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('RTT (s)')
            plt.show()
            print('')

            times = []
            for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
            for i in data:
                if(startTime<=i[0] and i[0]<endTime):
                    times[math.floor((i[0]-startTime)/bin)].append(i[1])
            effectiveTime = []
            for i, packets in enumerate(times):
                if len(packets)!=0:
                    effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                else:
                    effectiveTime.append([startTime+i*bin, 0])
            plt.scatter([j[0] for j in effectiveTime], [j[1] for j in effectiveTime], s=4, color='green')
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('RTT (s)')
            plt.show()

            return effectiveTime

    def getClientsTimeSeries(self, startTime, endTime, bin=0):
        if len(self.clientsRTT) == 0 and self.noRTT == False:
            self.processClientsRTT()
            if  len(self.clientsRTT) == 0:
                self.noRTT = True
        timeSeries = []
        if bin!=0:
            for index, data in enumerate(self.clientsRTT):
                times = []
                for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
                for i in data:
                    if(startTime<=i[0] and i[0]<endTime):
                        times[math.floor((i[0]-startTime)/bin)].append(i[1])
                effectiveTime = []
                for i, packets in enumerate(times):
                    if len(packets)!=0:
                        effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                    else:
                        effectiveTime.append([startTime+i*bin, 0])
                timeSeries.append(effectiveTime)
                plt.scatter([j[0] for j in effectiveTime], [j[1] for j in effectiveTime], s=4, color=self.colors[index], label=self.labels[index])
            plt.legend()
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('RTT (s)')
            plt.show()
            
            return timeSeries
        else :
            print('Please specify bin')

