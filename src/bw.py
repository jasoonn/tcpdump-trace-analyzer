from packet import packet
import math
import matplotlib.pyplot as plt

class bw:
    def __init__(self, packets, baseTime, desiredArr, outputFile, colors, labels):
        self.uploadBW = []
        self.downloadBW = []
        self.desiredArr = desiredArr
        self.outputFile = outputFile
        self.allMaxLen = []
        self.colors = colors
        self.labels = labels
        self.baseTime = baseTime
        self.packets = packets
        maxTime = packets[-1].getTime()
        self.arrLen = math.ceil(maxTime-baseTime)
        self.maxTime = self.arrLen + 1
        self.allUpBW = []
        self.allDownBW = []

        totalUpload = 0
        totalDownload = 0
        avgUpBW = []
        avgDownBW = []
        lengthBW = 0
        print("Process Bandwidth")
        #Process basic paire
        for IPPair in desiredArr:
            idx = 0
            upCount = 0   #Total Upload Bandwidth
            downCount = 0 #Total Download Bandwidth
            upBW = []
            downBW = []
            for i in range(self.arrLen):
                upBW.append([i, 0])
                downBW.append([i, 0])
            startTime = 0
            endTime = 0
            #(0~1] count in [0,?], (1~2] count in [1, ?]
            for i, packet in enumerate(packets):
                if (i%200 ==0):
                    print([IPPair ,i], end="\r", flush=True)
                if packet.checkIP(IPPair[0], IPPair[1])==False:
                    continue
                if (packet.getTime() - baseTime) > idx+1:
                    upBW[idx][1] = upCount
                    downBW[idx][1] = downCount
                    idx = math.floor(packet.getTime() - baseTime)
                    upCount = 0
                    downCount = 0
                if packet.getSender(True).find(IPPair[0]) == 0:
                    upCount += packet.getLen()
                    totalUpload += packet.getLen()
                else:
                    downCount += packet.getLen()
                    totalDownload += packet.getLen()
                if endTime ==0:
                    startTime = math.floor(packet.getTime() - self.baseTime)
                endTime = math.ceil(packet.getTime() - self.baseTime)

            #Choose interval between effective packets
            self.allUpBW.append(upBW)
            self.allDownBW.append(downBW)
            maxLen = endTime - startTime
            self.allMaxLen.append(maxLen)
            self.uploadBW.append(upBW[startTime:endTime])
            self.downloadBW.append(downBW[startTime:endTime])
            print(IPPair)
            print('Last period:', endTime - startTime, startTime, endTime)
            print("Upload sum:", sum([i[1] for i in upBW[startTime:endTime]])/1024, "KB", "Download sum:", sum([i[1] for i in downBW[startTime:endTime]])/1024, "KB")
            print('Avg upload BW:', sum([i[1] for i in upBW[startTime:endTime]])/len(upBW[startTime:endTime]), 'Avg download:',sum([i[1] for i in downBW[startTime:endTime]])/len(downBW[startTime:endTime]))
            avgUpBW.append(sum([i[1] for i in upBW[startTime:endTime]]))
            avgDownBW.append(sum([i[1] for i in downBW[startTime:endTime]]))
            lengthBW += endTime - startTime
        print("Avg total UP BW:", sum(avgUpBW)/lengthBW)
        print("Avg total DOWN BW:", sum(avgDownBW)/lengthBW)
        #Process accumulated
        print("Total Upload:", totalUpload/1024, "Kb", "Total Download:", totalDownload/1024)
        self.allUpAccumulated = []
        self.allDownAccumulated = []
        self.maxLim = 100000
        for index, (uploadData, downLoadData, IPPair) in enumerate(zip(self.uploadBW, self.downloadBW, self.desiredArr)):

            upAccumulated = []
            downAccumulated = []
            
            for i in range(self.maxLim):
                upAccumulated.append(0)
                downAccumulated.append(0)
            for (up, down) in zip(uploadData, downLoadData):
                if up[1]<self.maxLim:
                    upAccumulated[math.floor(up[1])] += 1
                if down[1]<self.maxLim:
                    downAccumulated[math.floor(down[1])] += 1
            
            for i in range(self.maxLim-1):
                upAccumulated[i+1] += upAccumulated[i]
                downAccumulated[i+1] += downAccumulated[i]

            self.allUpAccumulated.append(upAccumulated)
            self.allDownAccumulated.append(downAccumulated)

    def processSpecificPairs(self, IPpairData):
        allUp = []
        allDown = []
        for pairData in IPpairData:
            idx = 0
            upCount = 0   #Total Upload Bandwidth
            downCount = 0 #Total Download Bandwidth
            upBW = []
            downBW = []
            for i in range(self.arrLen):
                upBW.append([i, 0])
                downBW.append([i, 0])
            startTime = 0
            endTime = 0
            #(0~1] count in [0,?], (1~2] count in [1, ?]
            for i, packet in enumerate(self.packets):
                if (i%200 ==0):
                    print([pairData[0] ,i], end="\r", flush=True)
                if packet.checkIP(pairData[0][0], pairData[0][1])==False or (packet.getTime()-self.baseTime) < pairData[1] or (packet.getTime()-self.baseTime) > pairData[2]:
                    continue
                if (packet.getTime() - self.baseTime) > idx+1:
                    upBW[idx][1] = upCount
                    downBW[idx][1] = downCount
                    idx = math.floor(packet.getTime() - self.baseTime)
                    upCount = 0
                    downCount = 0
                if packet.getSender(True).find(pairData[0][0]) == 0:
                    upCount += packet.getLen()
                else:
                    downCount += packet.getLen()
                if endTime ==0:
                    startTime = math.floor(packet.getTime() - self.baseTime)
                endTime = math.ceil(packet.getTime() - self.baseTime)

            #Choose interval between effective packets
            maxLen = endTime - startTime
            self.allMaxLen.append(maxLen)
            for i in upBW[startTime:endTime]:
                allUp.append(i[1])
            for i in downBW[startTime:endTime]:
                allDown.append(i[1])
            print(pairData[0])
            print('Last period:', endTime - startTime, startTime, endTime)
            print("Upload sum:", sum([i[1] for i in upBW[startTime:endTime]])/1024, "KB", "Download sum:", sum([i[1] for i in downBW[startTime:endTime]])/1024, "KB")
            print('Avg upload BW:', sum([i[1] for i in upBW[startTime:endTime]])/len(upBW[startTime:endTime])/1024, 'Avg download:',sum([i[1] for i in downBW[startTime:endTime]])/len(downBW[startTime:endTime])/1024)
            print("")
        print("Overall BW upload", sum(allUp)/len(allUp), "download:", sum(allDown)/len(allDown))
        print("upload max:", max(allUp), "length", len(allUp))
        print("download max:", max(allDown), "length", len(allDown))
        upAcc = []
        downAcc = []
        for i in range(max([max(allUp), max(allDown)])+1):
            upAcc.append(0)
            downAcc.append(0)
        for i in allUp:
            upAcc[i] += 1
        for i in allDown:
            downAcc[i] += 1
        for i in range(max([max(allUp), max(allDown)])):
            upAcc[i+1] += upAcc[i]
            downAcc[i+1] += downAcc[i]
        print("Counts:", upAcc[-1], downAcc[-1])
        return (upAcc, downAcc)

    def plotTimeSeries(self, startTime, endTime, bin = 0):
        if bin != 0:
            #Upload
            for index, upBW in enumerate(self.allUpBW):
                times = []
                sum = 0
                for i, bwUnit in enumerate(upBW):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                plt.plot([j[0] for j in times], [j[1] for j in times], color=self.colors[index], linewidth = 1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            #plt.ylim(0, 15000)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWUpload" + ".png") 
            plt.show()
                    
            for index, upBW in enumerate(self.allUpBW):
                times = []
                sum = 0
                for i, bwUnit in enumerate(upBW):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                plt.scatter([j[0] for j in times], [j[1] for j in times], color=self.colors[index], s=4, label = self.labels[index])
            plt.xlim(startTime, endTime)
            #plt.ylim(0, 15000)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWUploadScatter" + ".png") 
            plt.show()

            #Download
            for index, downBW in enumerate(self.allDownBW):
                times = []
                sum = 0
                for i, bwUnit in enumerate(downBW):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                plt.plot([j[0] for j in times], [j[1] for j in times], color=self.colors[index], linewidth = 1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            #plt.ylim(0, 60000)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWDownload" + ".png") 
            plt.show()
                    
            for index, downBW in enumerate(self.allDownBW):
                times = []
                sum = 0
                for i, bwUnit in enumerate(downBW):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                plt.scatter([j[0] for j in times], [j[1] for j in times], color=self.colors[index], s=4, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            #plt.ylim(0, 60000)
            plt.ylabel('Bandwidth (bit/sec)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWDownloadScatter" + ".png") 
            plt.show()
        else:
            for index, upBW in enumerate(self.allUpBW):
                plt.plot([j[0] for j in upBW], [k[1] for k in upBW], color=self.colors[index], linestyle='dashed', linewidth = 1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWUpload" + ".png") 
            plt.show()

            for index, downBW in enumerate(self.allDownBW):
                plt.plot([j[0] for j in downBW], [k[1] for k in downBW], color=self.colors[index], linestyle='dashed', linewidth = 1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWDownload" + ".png") 
            plt.show()

            for index, upBW in enumerate(self.allUpBW):
                plt.scatter([j[0] for j in upBW], [k[1] for k in upBW], color=self.colors[index], s=1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWUploadScatter" + ".png") 
            plt.show()

            for index, downBW in enumerate(self.allDownBW):
                plt.scatter([j[0] for j in downBW], [k[1] for k in downBW], color=self.colors[index], s=1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWDownloadScatter" + ".png") 
            plt.show()


        

        #For filter zero
        # for index, downBW in enumerate(self.allDownBW):
        #     filterZero = []
        #     for i in downBW:
        #         if i[1]!=0:
        #             filterZero.append(i)
        #     plt.scatter([j[0] for j in filterZero], [k[1] for k in filterZero], color=self.colors[index], s=1, label = self.labels[index])
        # plt.xlim(startTime, endTime)
        # plt.xlabel('Time (s)')
        # plt.ylabel('Bandwidth (bit/sec)')
        # plt.legend()
        # plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWDownloadScatter" + ".png") 
        # plt.show()

        # for index, upBW in enumerate(self.allUpBW):
        #     filterZero = []
        #     for i in upBW:
        #         if i[1]!=0:
        #             filterZero.append(i)
        #     plt.scatter([j[0] for j in filterZero], [k[1] for k in filterZero], color=self.colors[index], s=1, label = self.labels[index])
        # plt.xlim(startTime, endTime)
        # plt.xlabel('Time (s)')
        # plt.ylabel('Bandwidth (bit/sec)')
        # plt.legend()
        # plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeBWUploadScatter" + ".png") 
        # plt.show()

    def plotTogether(self):
        for index, (upAccumulated, length) in enumerate(zip(self.allUpAccumulated, self.allMaxLen)):
            plt.plot([j for j in range(len(upAccumulated))], [k/(length) for k in upAccumulated], color=self.colors[index], label = self.labels[index])
        plt.xlim(0, self.maxLim)
        plt.xlabel('Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "UploadBWAll_CDF" + ".png") 
        plt.show()

        plt.xscale('log')
        for index, (upAccumulated, length) in enumerate(zip(self.allUpAccumulated, self.allMaxLen)):
            plt.plot([j for j in range(len(upAccumulated))], [k/(length) for k in upAccumulated], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "UploadBWAllxlog_CDF" + ".png") 
        plt.show()                  

        for index, (downAccumulated, length) in enumerate(zip(self.allDownAccumulated, self.allMaxLen)):
            plt.plot([j for j in range(len(downAccumulated))], [k/(length) for k in downAccumulated], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "DownloadBWAll_CDF" + ".png") 
        plt.show()   

        plt.xscale('log')
        for index, (downAccumulated, length) in enumerate(zip(self.allDownAccumulated, self.allMaxLen)):
            plt.plot([j for j in range(len(downAccumulated))], [k/(length) for k in downAccumulated], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "DownloadBWAllxlog_CDF" + ".png") 
        plt.show()    

    def plotDivide(self):
        for index, (upAccumulated, downAccumulated, IPPair, allTime) in enumerate(zip(self.allUpAccumulated, self.allDownAccumulated, self.desiredArr, self.allMaxLen)):
            plt.plot([j for j in range(len(upAccumulated))], [k/allTime for k in upAccumulated],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Upload BW CDF")
            plt.plot([j for j in range(len(downAccumulated))], [k/allTime for k in downAccumulated],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Download BW CDF")
            plt.xlim(0.1, self.maxLim)
            plt.xlabel('Time (s)')
            plt.ylabel('CDF')
            plt.legend()
            plt.savefig(self.outputFile + "BW_CDF" + IPPair[0] + "_" + IPPair[1] + ".png") 
            plt.show()

            plt.xscale('log')
            plt.plot([j for j in range(len(upAccumulated))], [k/(allTime-1) for k in upAccumulated],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Upload BW CDF")
            plt.plot([j for j in range(len(downAccumulated))], [k/(allTime-1) for k in downAccumulated],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Download BW CDF")
            plt.xlim(0.1, self.maxLim)
            plt.xlabel('Time (s)')
            plt.ylabel('CDF')
            plt.legend()
            plt.savefig(self.outputFile + "BW_CDF" + IPPair[0] + "_" + IPPair[1] + "xlog" + ".png") 
            plt.show()

    def plotSpecificServer(self, packets, serverIP):
        idx = 0
        uploadBW = 0
        downloadBW = 0
        upCount = 0
        downCount = 0
        upBW = []
        downBW = []
        for i in range(self.arrLen):
            upBW.append([i, 0])
            downBW.append([i, 0])
        startTime = 0
        endTime = 0
        for i, packet in enumerate(packets):
            if (i%200 ==0):
                print([serverIP ,i], end="\r", flush=True)
            if packet.checkIP(serverIP)==False:
                continue
            if (packet.getTime() - self.baseTime) > idx+1:
                upBW[idx][1] = upCount
                downBW[idx][1] = downCount
                idx = math.floor(packet.getTime() - self.baseTime)
                upCount = 0
                downCount = 0
            #Look from the clients' point of view for easy comparing
            if packet.getSender(True).find(serverIP) == 0:
                downCount += packet.getLen()
                downloadBW += packet.getLen()
            else:
                upCount += packet.getLen()
                uploadBW += packet.getLen()
            if endTime ==0:
                startTime = math.floor(packet.getTime() - self.baseTime)
            endTime = math.ceil(packet.getTime() - self.baseTime) 
        print("")
        print('Upload(Kb):', uploadBW/1024 , 'Download:', downloadBW/1024)

        #Choose interval between effective packets
        maxLen = endTime - startTime
        downBW = downBW[startTime:endTime]
        upBW = upBW[startTime:endTime]

        #Plot individual time series
        plt.plot([j[0] for j in upBW], [k[1] for k in upBW],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='green', markersize=0.2, label = "To server BW")
        plt.plot([j[0] for j in downBW], [k[1] for k in downBW],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Leave server BW")
        plt.xlim(0, self.maxTime)
        plt.xlabel('Time (s)')
        plt.ylabel('Bandwidth (bit/sec)')
        plt.legend()
        plt.savefig(self.outputFile + "_" + serverIP + "_timeBW" + ".png") 
        plt.show()

        upAccumulated = []
        downAccumulated = []
        
        for i in range(self.maxLim):
            upAccumulated.append(0)
            downAccumulated.append(0)
        for (up, down) in zip(upBW, downBW):
            if up[1]<self.maxLim:
                upAccumulated[math.floor(up[1])] += 1
            if down[1]<self.maxLim:
                downAccumulated[math.floor(down[1])] += 1
        
        for i in range(self.maxLim-1):
            upAccumulated[i+1] += upAccumulated[i]
            downAccumulated[i+1] += downAccumulated[i]
            
        plt.plot([j for j in range(len(upAccumulated))], [k/(maxLen) for k in upAccumulated], color='green', label = 'To server BW')
        plt.plot([j for j in range(len(downAccumulated))], [k/(maxLen) for k in downAccumulated], color='red', label = 'Leave server BW')
        plt.xlabel('Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "BW_CDF" + serverIP + ".png") 
        plt.show()

        plt.xscale('log')
        plt.plot([j for j in range(len(upAccumulated))], [k/(maxLen) for k in upAccumulated], color='green', label = 'To server BW')
        plt.plot([j for j in range(len(downAccumulated))], [k/(maxLen) for k in downAccumulated], color='red', label = 'Leave server BW')
        plt.xlabel('Time (s)')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "BW_CDFxlog" + serverIP + ".png") 
        plt.show()

    def getClientsBW(self, bin=0):
        if bin != 0:
            #Upload
            uploadTimes = []
            downloadTimes = []
            for index, upBW in enumerate(self.allUpBW):
                times = []
                sum = 0
                for i, bwUnit in enumerate(upBW):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                uploadTimes.append(times)

            #Download
            for index, downBW in enumerate(self.allDownBW):
                times = []
                sum = 0
                for i, bwUnit in enumerate(downBW):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                downloadTimes.append(times)

            return (uploadTimes, downloadTimes)

    def getServerBW(self, serverIP, bin = 0):
        idx = 0
        uploadBW = 0
        downloadBW = 0
        upCount = 0
        downCount = 0
        upBW = []
        downBW = []
        for i in range(self.arrLen):
            upBW.append([i, 0])
            downBW.append([i, 0])
        for i, packet in enumerate(self.packets):
            if (i%200 ==0):
                print([serverIP ,i], end="\r", flush=True)
            if packet.checkIP(serverIP)==False:
                continue
            if (packet.getTime() - self.baseTime) > idx+1:
                upBW[idx][1] = upCount
                downBW[idx][1] = downCount
                idx = math.floor(packet.getTime() - self.baseTime)
                upCount = 0
                downCount = 0
            #Look from the clients' point of view for easy comparing
            if packet.getSender(True).find(serverIP) == 0:
                downCount += packet.getLen()
                downloadBW += packet.getLen()
            else:
                upCount += packet.getLen()
                uploadBW += packet.getLen()
        print("")
        print('Upload(Kb):', uploadBW/1024 , 'Download:', downloadBW/1024)

        if bin != 0:
            #Upload
            upTimes = []
            sum = 0
            for i, bwUnit in enumerate(upBW):
                if i%bin ==0 and i!=0:
                    upTimes.append([bwUnit[0]-bin, sum/bin])
                    sum = 0
                sum += bwUnit[1]
            plt.plot([j[0] for j in upTimes], [j[1] for j in upTimes], color='green', linewidth = 1)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.savefig(self.outputFile + "_" + serverIP + "BWUpload" + ".png") 
            plt.show()

            #Download
            downTimes = []
            sum = 0
            for i, bwUnit in enumerate(downBW):
                if i%bin ==0 and i!=0:
                    downTimes.append([bwUnit[0]-bin, sum/bin])
                    sum = 0
                sum += bwUnit[1]
            plt.plot([j[0] for j in downTimes], [j[1] for j in downTimes], color='green', linewidth = 1)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.savefig(self.outputFile + "_" + serverIP + "BWDownload" + ".png") 
            plt.show()

            return (upTimes, downTimes)



    def getOverallBW(self, bin=0):
        idx = 0
        uploadBW = 0
        downloadBW = 0
        upCount = 0
        downCount = 0
        upBW = []
        downBW = []
        upNum = 0
        downNum = 0
        for i in range(self.arrLen):
            upBW.append([i, 0])
            downBW.append([i, 0])
        for i, packet in enumerate(self.packets):
            if (i%200 ==0):
                print(i, end="\r", flush=True)
            if (packet.getTime() - self.baseTime) > idx+1:
                upBW[idx][1] = upCount
                downBW[idx][1] = downCount
                idx = math.floor(packet.getTime() - self.baseTime)
                upCount = 0
                downCount = 0
            #Look from the clients' point of view for easy comparing
            if packet.getSender(True).find('192.168.1') == 0:
                upCount += packet.getLen()
                uploadBW += packet.getLen()
                upNum +=1
            else:
                downCount += packet.getLen()
                downloadBW += packet.getLen()
                downNum += 1
        print("")
        print('Upload(Kb):', uploadBW/1024 , 'Download:', downloadBW/1024)
        print('Upload packetNum', upNum, 'Download packetNum', downNum)

        if bin != 0:
            #Upload
            upTimes = []
            sum = 0
            for i, bwUnit in enumerate(upBW):
                if i%bin ==0 and i!=0:
                    upTimes.append([bwUnit[0]-bin, sum/bin])
                    sum = 0
                sum += bwUnit[1]
            # plt.plot([j[0] for j in upTimes], [j[1] for j in upTimes], color='green', linewidth = 1)
            # plt.xlabel('Time (s)')
            # plt.ylabel('Bandwidth (bit/sec)')
            # plt.savefig(self.outputFile + "_" + "_overallBWUpload" + ".png") 
            # plt.show()

            #Download
            downTimes = []
            sum = 0
            for i, bwUnit in enumerate(downBW):
                if i%bin ==0 and i!=0:
                    downTimes.append([bwUnit[0]-bin, sum/bin])
                    sum = 0
                sum += bwUnit[1]
            # plt.plot([j[0] for j in downTimes], [j[1] for j in downTimes], color='green', linewidth = 1)
            # plt.xlabel('Time (s)')
            # plt.ylabel('Bandwidth (bit/sec)')
            # plt.savefig(self.outputFile + "_" + "_overallBWDownload" + ".png") 
            # plt.show()

            return (upTimes, downTimes)
