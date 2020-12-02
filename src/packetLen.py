from packet import packet
import math
import matplotlib.pyplot as plt
import csv

class packetLen:
    def __init__(self, packets, desiredArr, outputFile, colors, labels, baseTime, generateOverAll=False):
        self.colors = colors
        self.labels = labels
        self.packets = packets
        self.outputFile = outputFile
        self.allUploadArr = []
        self.allDownloadArr = []
        self.allUploadCount = []
        self.allDownloadCount = []
        self.maxPacketLenth = 0
        self.timeUploadArr = []
        self.timeDownloadArr = []
        self.baseTime = baseTime
        # Average data
        print("Process Packet Length")
        #Get biggest packet size
        for i in packets:
            if i.getLen() > self.maxPacketLenth:
                self.maxPacketLenth = i.getLen()


        for IPPair in desiredArr:
            lenUploadArr = []
            lenDownloadArr = []
            uploadTime = []
            downloadTime = []
            upCount = 0
            downCount = 0
            for i in range(self.maxPacketLenth+1):
                lenUploadArr.append(0)
                lenDownloadArr.append(0)

            for i, packet in enumerate(packets):
                if (i%200 ==0):
                    print([IPPair ,i], end="\r", flush=True)
                if packet.checkIP(IPPair[0], IPPair[1])==False:
                    continue
                if packet.getSender(True).find(IPPair[0]) == 0:
                    lenUploadArr[packet.getLen()] +=1
                    upCount += 1
                    uploadTime.append([packet.getTime()-baseTime, packet.getLen()])
                else:
                    lenDownloadArr[packet.getLen()] +=1
                    downCount += 1
                    downloadTime.append([packet.getTime()-baseTime, packet.getLen()])
            #Accumulated
            for i in range(self.maxPacketLenth):
                lenUploadArr[i+1] += lenUploadArr[i]
                lenDownloadArr[i+1] += lenDownloadArr[i]

            self.allUploadArr.append(lenUploadArr)
            self.allDownloadArr.append(lenDownloadArr)
            self.allUploadCount.append(upCount)
            self.allDownloadCount.append(downCount)
            self.timeUploadArr.append(uploadTime)
            self.timeDownloadArr.append(downloadTime)


        print("")

        if generateOverAll ==True:
            print("general all")
            lenUploadArr = []
            lenDownloadArr = []
            upSizeCount = 0
            downSizeCount = 0
            for i in range(self.maxPacketLenth+1):
                lenUploadArr.append(0)
                lenDownloadArr.append(0)
            for IPPair in desiredArr:
                for i, packet in enumerate(packets):
                    if (i%200 ==0):
                        print([IPPair ,i], end="\r", flush=True)
                    if packet.checkIP(IPPair[0], IPPair[1])==False:
                        continue
                    if packet.getSender(True).find(IPPair[0]) == 0:
                        lenUploadArr[packet.getLen()] +=1
                        upSizeCount += packet.getLen()
                    else:
                        lenDownloadArr[packet.getLen()] +=1
                        downSizeCount += packet.getLen()
             #Accumulated
            for i in range(self.maxPacketLenth):
                lenUploadArr[i+1] += lenUploadArr[i]
                lenDownloadArr[i+1] += lenDownloadArr[i]
            print("")
            print("Upload:", lenUploadArr[-1], "Download:", lenDownloadArr[-1])
            print("avg upload", upSizeCount/lenUploadArr[-1], "avg download", downSizeCount/lenDownloadArr[-1])
            print("Overall avg", (upSizeCount+downSizeCount)/(lenUploadArr[-1]+lenDownloadArr[-1]))
            #with open('Packetlen.csv', 'w', newline='') as csvfile:


    def processSpecificPairs(self, IPpairData):
        lenUploadArr = []
        lenDownloadArr = []
        upCount = 0
        downCount = 0
        totalLen = 0
        for i in range(self.maxPacketLenth):
            lenUploadArr.append(0)
            lenDownloadArr.append(0)
        for IPPair in IPpairData:

            for i, packet in enumerate(self.packets):
                if (i%200 ==0):
                    print([IPPair[0] ,i], end="\r", flush=True)
                if packet.checkIP(IPPair[0][0], IPPair[0][1])==False or (packet.getTime()-self.baseTime) < IPPair[1] or (packet.getTime()-self.baseTime) > IPPair[2]:
                    continue
                if packet.getSender(True).find(IPPair[0][0]) == 0:
                    totalLen += packet.getLen()
                    lenUploadArr[packet.getLen()] +=1
                    upCount += 1
                else:
                    totalLen += packet.getLen()
                    lenDownloadArr[packet.getLen()] +=1
                    downCount += 1
        print("")
        print("process specific pair average", totalLen/(upCount+downCount))
        #Accumulated
        for i in range(self.maxPacketLenth-1):
            lenUploadArr[i+1] += lenUploadArr[i]
            lenDownloadArr[i+1] += lenDownloadArr[i]

        
        return (lenUploadArr, lenDownloadArr)



    def plotSpecificServer(self, packets, serverIP):
        lenUploadArr = []
        lenDownloadArr = []
        upCount = 0
        downCount = 0
        for i in range(self.maxPacketLenth):
            lenUploadArr.append(0)
            lenDownloadArr.append(0)
        for i, packet in enumerate(packets):
            if (i%200 ==0):
                print([serverIP ,i], end="\r", flush=True)
            if packet.checkIP(serverIP)==False:
                continue
            # Download & Upload base on clients for easy comparison to other plots
            if packet.getSender(True).find(serverIP) == 0:
                lenDownloadArr[packet.getLen()] +=1
                downCount += 1
            else:
                lenUploadArr[packet.getLen()] +=1
                upCount += 1
        
        for i in range(self.maxPacketLenth-1):
                lenUploadArr[i+1] += lenUploadArr[i]
                lenDownloadArr[i+1] += lenDownloadArr[i]

        
        print("Upload packets:", upCount, "Download packets:", downCount)
        plt.plot([j for j in range(len(lenUploadArr))], [k/upCount for k in lenUploadArr],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "To server")
        plt.plot([j for j in range(len(lenDownloadArr))], [k/downCount for k in lenDownloadArr],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Leave server")
        plt.xlabel('Packet size')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_packetSize" + serverIP + ".png") 
        plt.show()

        plt.xscale('log')
        print("Upload packets:", upCount, "Download packets:", downCount)
        plt.plot([j for j in range(len(lenUploadArr))], [k/upCount for k in lenUploadArr],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "To server")
        plt.plot([j for j in range(len(lenDownloadArr))], [k/downCount for k in lenDownloadArr],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Leave server")
        plt.xlabel('Packet size')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_packetSizexlog" + serverIP + ".png") 
        plt.show()

    def plotDivide(self):
        for index, (upCount, lenUploadArr, downCount, lenDownloadArr) in enumerate(zip(self.allUploadCount, self.allUploadArr, self.allDownloadCount, self.allDownloadArr)):
            plt.plot([j for j in range(len(lenUploadArr))], [k/upCount for k in lenUploadArr],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Upload")
            plt.plot([j for j in range(len(lenDownloadArr))], [k/downCount for k in lenDownloadArr],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Download")
            plt.xlabel('Packet size')
            plt.ylabel('CDF')
            plt.legend()
            plt.savefig(self.outputFile + "_packetSize" + ".png") 
            plt.show()

            plt.xscale('log')
            plt.plot([j for j in range(len(lenUploadArr))], [k/upCount for k in lenUploadArr],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Upload")
            plt.plot([j for j in range(len(lenDownloadArr))], [k/downCount for k in lenDownloadArr],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Download")
            plt.xlabel('Packet size')
            plt.ylabel('CDF')
            plt.legend()
            plt.savefig(self.outputFile + "_packetSizeXlog" + ".png") 
            plt.show()

    def plotTogether(self):
        for index, (upCount, lenUploadArr) in enumerate(zip(self.allUploadCount, self.allUploadArr)):
            plt.plot([j for j in range(len(lenUploadArr))], [k/upCount for k in lenUploadArr], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Packet len')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_packetlenUploadAll" + ".png") 
        plt.show()

        plt.xscale('log')
        for index, (upCount, lenUploadArr) in enumerate(zip(self.allUploadCount, self.allUploadArr)):
            plt.plot([j for j in range(len(lenUploadArr))], [k/upCount for k in lenUploadArr], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Packet len')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_packetlenUploadAllxlog" + ".png") 
        plt.show()

        for index, (downCount, lenDownloadArr) in enumerate(zip(self.allDownloadCount, self.allDownloadArr)):
            plt.plot([j for j in range(len(lenDownloadArr))], [k/downCount for k in lenDownloadArr], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Packet len')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_packetlenDwnloadAll" + ".png") 
        plt.show()

        plt.xscale('log')
        for index, (downCount, lenDownloadArr) in enumerate(zip(self.allDownloadCount, self.allDownloadArr)):
            plt.plot([j for j in range(len(lenDownloadArr))], [k/downCount for k in lenDownloadArr], color=self.colors[index], label = self.labels[index])
        plt.xlabel('Packet len')
        plt.ylabel('CDF')
        plt.legend()
        plt.savefig(self.outputFile + "_packetlenDwnloadAllxlog" + ".png") 
        plt.show()

    def plotSpecificTimeSeries(self, startTime=0, endTime=-1, serverIP='130.211.14.80', clientIP=""):
        if endTime == -1:
            endTime = math.ceil(self.packets[-1].getTime()-self.baseTime)

        packetsUpload = []
        packetsDownload = []
        for i, packet in enumerate(self.packets):
            packetTime = packet.getTime()-self.baseTime
            if (i%500 ==0):
                print(i, end="\r", flush=True)
            if packetTime<startTime or packetTime>endTime:
                continue
            if packet.getRecv(True).find(serverIP) == 0 and packet.getSender(True).find(clientIP) == 0:
                packetsUpload.append([packetTime, packet.getLen()])
            if packet.getSender(True).find(serverIP) == 0 and packet.getRecv(True).find(clientIP) == 0:
                packetsDownload.append([packetTime, packet.getLen()])

        if len(packetsUpload) == 0 and len(packetsDownload) == 0:
            return
        plt.scatter([packet[0] for packet in packetsUpload], [packet[1] for packet in packetsUpload], s=8, color='green', label = serverIP + '_' + clientIP + '_Upload')
        plt.scatter([packet[0] for packet in packetsDownload], [packet[1] for packet in packetsDownload], s=8, color='blue', label = serverIP + '_' + clientIP + '_Download')
        plt.xlabel('Time (s)')
        plt.ylabel('Packet Size')
        plt.xlim(startTime, endTime)
        plt.ylim(-10, 1500)
        plt.legend()
        plt.savefig(self.outputFile + "_" + str(startTime/1000) + "_" + clientIP + "_packetNum.png")
        plt.close()

    def plotTimeSeries(self, startTime, endTime, bin=0):
        if bin!=0:
            for index, upLength in enumerate(self.timeUploadArr):
                times = []
                sum = 0
                for i, bwUnit in enumerate(upLength):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                plt.plot([j[0] for j in times], [j[1] for j in times], color=self.colors[index], linewidth = 1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Length (Byte)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeLengthUpload" + ".png") 
            plt.show()

            for index, upLength in enumerate(self.timeUploadArr):
                times = []
                sum = 0
                for i, bwUnit in enumerate(upLength):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                plt.scatter([j[0] for j in times], [j[1] for j in times], color=self.colors[index], s = 2, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Length (Byte)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeLengthUploadScatter" + ".png") 
            plt.show()

            for index, downLength in enumerate(self.timeDownloadArr):
                times = []
                sum = 0
                for i, bwUnit in enumerate(downLength):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                plt.plot([j[0] for j in times], [j[1] for j in times], color=self.colors[index], linewidth = 1, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Length (Byte)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeLengthDownload" + ".png") 
            plt.show()

            for index, downLength in enumerate(self.timeDownloadArr):
                times = []
                sum = 0
                for i, bwUnit in enumerate(downLength):
                    if i%bin ==0 and i!=0:
                        times.append([bwUnit[0]-bin, sum/bin])
                        sum = 0
                    sum += bwUnit[1]
                plt.scatter([j[0] for j in times], [j[1] for j in times], color=self.colors[index], s = 2, label = self.labels[index])
            plt.xlim(startTime, endTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Length (Byte)')
            plt.legend()
            plt.savefig(self.outputFile + "_" + str(startTime/500) + "_timeLengthDownloadScatter" + ".png") 
            plt.show()
