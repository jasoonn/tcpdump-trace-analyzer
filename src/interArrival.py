from packet import packet
import math
import matplotlib.pyplot as plt


class interArrival():

    def __init__(self, packets, desiredArr, outputFile, colors, labels, baseTime):
        self.outputFile = outputFile
        self.desiredArr = desiredArr
        self.colors = colors
        self.labels = labels
        self.baseTime = baseTime
        self.allUploadAcc = []
        self.packets = packets
        self.allDownloadAcc = []
        self.allUploadCount = []
        self.allDownloadCount = []
        self.allTimeUpload = []
        self.allTimeDownload = []
        self.maxTime = math.ceil(packets[-1].getTime()-baseTime)
        print(self.maxTime)
        print("Process Inter Arrival Time")

        sumTime = []
        for IPPair in desiredArr:
            upTimeList = []
            downTimeList = []

            upPrevTime = -1
            downPrevTime = -1
            for i, packet in enumerate(packets):
                if (i%200 ==0):
                    print([IPPair ,i], end="\r", flush=True)
                if packet.checkIP(IPPair[0], IPPair[1])==False:
                    continue
                if packet.getSender(True).find(IPPair[0]) == 0:
                    if upPrevTime != -1:
                        upTimeList.append([upPrevTime - baseTime, packet.getTime()-upPrevTime])
                        upPrevTime = packet.getTime()
                    else:
                        upPrevTime = packet.getTime()
                else:
                    if downPrevTime != -1:
                        downTimeList.append([downPrevTime - baseTime, packet.getTime()-downPrevTime])
                        downPrevTime = packet.getTime()
                    else:
                        downPrevTime = packet.getTime()
            maxInter = max([max([j[1] for j in upTimeList]), max([j[1] for j in downTimeList])])
            lim = min([maxInter, 20])
            print(lim)

            for i in upTimeList:
                sumTime.append(i[1])
            for i in downTimeList:
                sumTime.append(i[1])
            
            uploadInterArr = []
            downloadInterArr = []
            for i in [x*0.001 for x in range(int(math.ceil(lim)*1000))]:
                uploadInterArr.append([i, 0])
                downloadInterArr.append([i, 0])
            for up in upTimeList:
                if up[1] < lim:
                    uploadInterArr[math.floor(up[1]*1000)][1] += 1
            for down in downTimeList:
                if down[1] < lim:
                    downloadInterArr[math.floor(down[1]*1000)][1] += 1

            for i in range(math.ceil(lim)*1000-1):
                uploadInterArr[i+1][1] += uploadInterArr[i][1]
                downloadInterArr[i+1][1] += downloadInterArr[i][1]

            self.allUploadAcc.append(uploadInterArr)
            self.allDownloadAcc.append(downloadInterArr)
            self.allUploadCount.append(len(upTimeList))
            self.allDownloadCount.append(len(downTimeList))
            self.allTimeUpload.append(upTimeList)
            self.allTimeDownload.append(downTimeList)

        print("max:", max(sumTime))
        print("overall sumtime num", len(sumTime))
        print("Non filter:", sum(sumTime)/len(sumTime))
        lims = [20, 50, 75, 100, 150, 200, 400, 600]
        for i in lims:
            count = 0
            summ = 0
            for j in sumTime:
                if j<i:
                    count+=1
                    summ +=j
            print(i, "filter:", summ/count)

        print("")

    def processSpecificPairs(self, IPpairData):
        upTimeList = []
        downTimeList = []
        for pairData in IPpairData:
            upPrevTime = -1
            downPrevTime = -1
            for i, packet in enumerate(self.packets):
                if (i%200 ==0):
                    print([pairData[0] ,i], end="\r", flush=True)
                
                if packet.checkIP(pairData[0][0], pairData[0][1])==False or (packet.getTime()-self.baseTime) < pairData[1] or (packet.getTime()-self.baseTime) > pairData[2]:
                    continue
                if packet.getSender(True).find(pairData[0][0]) == 0:
                    if upPrevTime != -1:
                        upTimeList.append([upPrevTime - self.baseTime, packet.getTime()-upPrevTime])
                        upPrevTime = packet.getTime()
                    else:
                        upPrevTime = packet.getTime()
                else:
                    if downPrevTime != -1:
                        downTimeList.append([downPrevTime - self.baseTime, packet.getTime()-downPrevTime])
                        downPrevTime = packet.getTime()
                    else:
                        downPrevTime = packet.getTime()
        print("max:", max([max([j[1] for j in upTimeList]), max([j[1] for j in downTimeList])]))
        maxx = max([max([j[1] for j in upTimeList]), max([j[1] for j in downTimeList])])
        #maxx = 1
            
        uploadInterArr = []
        downloadInterArr = []
        for i in [x*0.005 for x in range(int(math.ceil(maxx)*200))]:
            uploadInterArr.append([i, 0])
            downloadInterArr.append([i, 0])
        for up in upTimeList:
            if math.ceil(up[1]*200) < int(math.ceil(maxx)*200):
                uploadInterArr[math.ceil(up[1]*200)][1] += 1
        for down in downTimeList:
            if math.ceil(down[1]*200) < int(math.ceil(maxx)*200):
                downloadInterArr[math.ceil(down[1]*200)][1] += 1

        for i in range(math.ceil(maxx)*200-1):
            uploadInterArr[i+1][1] += uploadInterArr[i][1]
            downloadInterArr[i+1][1] += downloadInterArr[i][1]


        return (uploadInterArr, len(upTimeList), downloadInterArr, len(downTimeList))
        

    def plotDivide(self):
        for index, (uploadInterArr, downloadInterArr, upCount, downCount) in enumerate(zip(self.allUploadAcc, self.allDownloadAcc, self.allUploadCount, self.allDownloadCount)):
            plt.plot([j[0] for j in uploadInterArr], [k[1]/upCount for k in uploadInterArr],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Uoload arrival time CDF")
            plt.plot([j[0] for j in downloadInterArr], [k[1]/downCount for k in downloadInterArr],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Download arrival time CDF")
            plt.xlabel('Inter-arrival Time (s)')
            plt.ylabel('CDF')
            plt.legend()
            plt.savefig(self.outputFile + "_interTime" + ".png") 
            plt.show()
                    
            plt.xscale('log')
            plt.plot([j[0] for j in uploadInterArr], [k[1]/upCount for k in uploadInterArr],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Uoload arrival time CDF")
            plt.plot([j[0] for j in downloadInterArr], [k[1]/downCount for k in downloadInterArr],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Download arrival time CDF")
            plt.xlabel('Inter-arrival Time (s)')
            plt.ylabel('CDF')
            plt.legend()
            plt.savefig(self.outputFile + "_interTimeXlog" + ".png") 
            plt.show()

    def plotSpecificServer(self, packets, serverIP):
        upInterList = []
        downInterList = []
        upPrevTime = -1
        downPrevTime = -1
        for i, packet in enumerate(packets):
            if (i%200 ==0):
                print([serverIP ,i], end="\r", flush=True)
            if packet.checkIP(serverIP)==False:
                continue
            #Look from the clients' point of view for easy comparing
            if packet.getSender(True).find(serverIP) == 0:
                if downPrevTime != -1:
                    downInterList.append(packet.getTime()-downPrevTime)
                    downPrevTime = packet.getTime()
                else:
                    downPrevTime = packet.getTime()
            else:
                if upPrevTime != -1:
                    upInterList.append(packet.getTime()-upPrevTime)
                    upPrevTime = packet.getTime()
                else:
                    upPrevTime = packet.getTime()

        maxInter = max([max(upInterList), max(downInterList)])
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

        for i in range(math.ceil(lim)*1000-1):
            uploadInterArr[i+1][1] += uploadInterArr[i][1]
            downloadInterArr[i+1][1] += downloadInterArr[i][1]
        
        plt.plot([j[0] for j in uploadInterArr], [k[1]/len(upInterList) for k in uploadInterArr], color='green', label = "To server")
        plt.plot([j[0] for j in downloadInterArr], [k[1]/len(downInterList) for k in downloadInterArr], color='red', label = "Leave server")
        plt.xlabel('Inter-arrival Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_interTime" + serverIP + ".png") 
        plt.show()

        plt.xscale('log')
        plt.plot([j[0] for j in uploadInterArr], [k[1]/len(upInterList) for k in uploadInterArr], color='green', label = "To server")
        plt.plot([j[0] for j in downloadInterArr], [k[1]/len(downInterList) for k in downloadInterArr], color='red', label = "Leave server")
        plt.xlabel('Inter-arrival Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_interTimexlog" + serverIP + ".png") 
        plt.show()


    def plotTimeSeries(self, startTime, endTime, bin=0):
        if bin!=0:
            for index, interTime in enumerate(self.allTimeUpload):
                times = []
                for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
                for i in interTime:
                    if(startTime<=i[0] and i[0]<endTime):
                        times[math.floor((i[0]-startTime)/bin)].append(i[1])
                effectiveTime = []
                for i, packets in enumerate(times):
                    if len(packets)!=0:
                        effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                plt.scatter([j[0] for j in effectiveTime], [k[1] for k in effectiveTime], color=self.colors[index], s=4, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.xlabel('Time(s)')
            plt.ylabel('Inter-arrival Time (s)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_interTimeUploadAllScatter" + ".png") 
            plt.show()

            for index, interTime in enumerate(self.allTimeUpload):
                times = []
                for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
                for i in interTime:
                    if(startTime<=i[0] and i[0]<endTime):
                        times[math.floor((i[0]-startTime)/bin)].append(i[1])
                effectiveTime = []
                for i, packets in enumerate(times):
                    if len(packets)!=0:
                        effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                plt.plot([j[0] for j in effectiveTime], [k[1] for k in effectiveTime], color=self.colors[index], linewidth = 1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.xlabel('Time(s)')
            plt.ylabel('Inter-arrival Time (s)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_interTimeUploadAll" + ".png") 
            plt.show()

            for index, interTime in enumerate(self.allTimeDownload):
                times = []
                for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
                for i in interTime:
                    if(startTime<=i[0] and i[0]<endTime):
                        times[math.floor((i[0]-startTime)/bin)].append(i[1])
                effectiveTime = []
                for i, packets in enumerate(times):
                    if len(packets)!=0:
                        effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                plt.scatter([j[0] for j in effectiveTime], [k[1] for k in effectiveTime], color=self.colors[index], s=4, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.xlabel('Time(s)')
            plt.ylabel('Inter-arrival Time (s)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_interTimeDownloadAllScatter" + ".png") 
            plt.show()

            for index, interTime in enumerate(self.allTimeDownload):
                times = []
                for _ in range(math.ceil((endTime-startTime)/bin)):
                    times.append([])
                for i in interTime:
                    if(startTime<=i[0] and i[0]<endTime):
                        times[math.floor((i[0]-startTime)/bin)].append(i[1])
                effectiveTime = []
                for i, packets in enumerate(times):
                    if len(packets)!=0:
                        effectiveTime.append([startTime+i*bin, sum(packets)/len(packets)])
                plt.plot([j[0] for j in effectiveTime], [k[1] for k in effectiveTime], color=self.colors[index], linewidth = 1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.xlabel('Time(s)')
            plt.ylabel('Inter-arrival Time (s)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_interTimeDownloadAll" + ".png") 
            plt.show()
        else:
            for index, interTime in enumerate(self.allTimeDownload):
                plt.scatter([j[0] for j in interTime], [k[1] for k in interTime], color=self.colors[index], s=1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.xlabel('Time(s)')
            plt.ylabel('Inter-arrival Time (s)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_interTimeUploadAll" + ".png") 
            plt.show()

            for index, interTime in enumerate(self.allTimeDownload):
                plt.scatter([j[0] for j in interTime], [k[1] for k in interTime], color=self.colors[index], s=1, label = self.labels[index])
            plt.xlabel('Time(s)')
            plt.xlim(startTime, endTime)
            plt.ylim(0, 1)
            plt.ylabel('Inter-arrival Time (s)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_interTimeDownloadAll" + ".png") 
            plt.show()

    def plotTogether(self):       

        for index, (uploadInterArr, upCount) in enumerate(zip(self.allUploadAcc, self.allUploadCount)):
            plt.plot([j[0] for j in uploadInterArr], [k[1]/upCount for k in uploadInterArr], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Inter-arrival Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_interTimeUploadAll" + ".png") 
        plt.show()

        plt.xscale('log')
        for index, (uploadInterArr, upCount) in enumerate(zip(self.allUploadAcc, self.allUploadCount)):
            plt.plot([j[0] for j in uploadInterArr], [k[1]/upCount for k in uploadInterArr], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Inter-arrival Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_interTimeUploadAllxlog" + ".png") 
        plt.show()

        for index, (downInterArr, downCount) in enumerate(zip(self.allDownloadAcc, self.allDownloadCount)):
            plt.plot([j[0] for j in downInterArr], [k[1]/downCount for k in downInterArr], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Inter-arrival Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_interTimeDownloadAll" + ".png") 
        plt.show()

        plt.xscale('log')
        for index, (downInterArr, downCount) in enumerate(zip(self.allDownloadAcc, self.allDownloadCount)):
            plt.plot([j[0] for j in downInterArr], [k[1]/downCount for k in downInterArr], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Inter-arrival Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_interTimeDownloadAllxlog" + ".png") 
        plt.show()

    def getACF(self, startTime=0, endTime=-1, sampleFreq=100, serverIP='130.211.14.80', clientIP=""):
        if endTime == -1:
            endTime = self.maxTime

        totalPoints = (endTime-startTime)*sampleFreq
        
        packetsCount = []
        for _ in range(totalPoints):
            packetsCount.append(0)
        countt = 0
        countLeave = 0
        for i, packet in enumerate(self.packets):
            packetTime = packet.getTime()-self.baseTime
            if (i%500 ==0):
                print(i, end="\r", flush=True)
            if packetTime<startTime or packetTime>endTime:
                continue
            if packet.getSender(True).find("192.168.1.18")==0 or packet.getSender(True).find("192.168.1.20")==0:
                continue
            #Look from the clients' point of view for easy comparing
            if packet.getRecv(True).find(serverIP) == 0 and packet.getSender(True).find(clientIP) == 0:
                countt +=1
                packetsCount[math.floor((packetTime-startTime)*sampleFreq)] += 1
            if packet.getSender(True).find(serverIP) == 0 and packet.getRecv(True).find(clientIP) == 0:
                countLeave += 1
        
        print('Total packetNum:', countt, countLeave)
        if countt==0:
            return
        
        # sin
        # packetsCount = []
        # for i in range(totalPoints):
        #     packetsCount.append(math.sin(i*0.01))
        # plt.plot([j/100 for j in range(totalPoints)], packetsCount)
        # plt.savefig(self.outputFile + "_sinTime.png")
        # plt.show()
        fig = plt.figure()
        plt.plot([startTime + j/sampleFreq for j in range(totalPoints)], packetsCount)
        plt.xlabel('Time (s)')
        plt.ylabel('PacketNum')
        plt.savefig(self.outputFile + "_" + str(startTime/100) + "_" + clientIP + "_packetNum.png")
        plt.close(fig)

        acf = []
        #Remove inactive data points
        for index, num in enumerate(packetsCount):
            if num!=0:
                packetsCount = packetsCount[index:]
                break
        for index, num in enumerate(reversed(packetsCount)):
            if num!=0:
                if index!=0:
                    packetsCount = packetsCount[:-index]
                break
        totalPoints = len(packetsCount)
        print("Effective time:", totalPoints/sampleFreq)

        mean = sum(packetsCount)/len(packetsCount)
        denominator = 0
        for i in packetsCount:
            denominator += math.pow((i-mean),2)
        print("mean:", mean, "denominator:", denominator)

        #Only plot for 100 second
        interestPoints = 100 * sampleFreq
        for k in range(1, interestPoints):
            if k%100 ==0:
                print(k)
            if k==0:
                continue
            numerator = 0
            for index in range(totalPoints-k):
                numerator += (packetsCount[index]-mean) * (packetsCount[k+index]-mean)
            acf.append(numerator/denominator)

        fig = plt.figure()
        plt.bar([j/sampleFreq for j in range(1, interestPoints)], acf, label=str(startTime)+'~'+str(endTime))
        plt.legend()
        plt.ylim(-0.1, 0.2)
        plt.savefig(self.outputFile + "_" + str(startTime/1000) + "_" + clientIP + "ACF.png")
        plt.close(fig)



