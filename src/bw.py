from Packet import Packet
import math
import matplotlib.pyplot as plt

class bw:
    def __init__(self, packets, baseTime, desiredArr, outputFile):
        self.uploadBW = []
        self.downloadBW = []
        self.desiredArr = desiredArr
        self.outputFile = outputFile
        maxTime = packets[-1].getTime()
        arrLen = math.ceil(maxTime-baseTime)
        self.maxTime = arrLen + 1
        totalUpload = 0
        totalDownload = 0
        
        for IPPair in desiredArr:
            idx = 1
            upCount = 0
            downCount = 0
            bandWidth = 0
            upBW = []
            downBW = []
            for i, packet in enumerate(packets):
                if (i%200 ==0):
                    print([IPPair ,i], end="\r", flush=True)
                if packet.checkIP(IPPair[0], IPPair[1])==False:
                    continue
                if (packet.getTime() - baseTime) >= idx:
                    upBW.append([idx, upCount])
                    downBW.append([idx, downCount])
                    idx += 1
                    upCount = 0
                    downCount = 0
                if packet.getSender(True).find(IPPair[0]) == 0:
                    upCount += packet.getLen()
                    totalUpload += packet.getLen()
                else:
                    downCount += packet.getLen()
                    totalDownload += packet.getLen()
            self.uploadBW.append(upBW)
            self.downloadBW.append(downBW)
        print("")
        print("Upload:", totalUpload/1024, "Kb")
        print("Download:", totalDownload/1024, "Kb")
        
    def plotDivide(self):
        for index, (uploadData, downLoadData, IPPair) in enumerate(zip(self.uploadBW, self.downloadBW, self.desiredArr)):
            plt.plot([j[0] for j in uploadData], [k[1] for k in uploadData],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2)
            plt.xlim(0, self.maxTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.savefig(self.outputFile + "_" + IPPair[0] + "_" + IPPair[1] + "_UploadBW" + ".png") 
            plt.show()

            plt.plot([j[0] for j in downLoadData], [k[1] for k in downLoadData],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2)
            plt.xlim(0, self.maxTime)
            plt.xlabel('Time (s)')
            plt.ylabel('Bandwidth (bit/sec)')
            plt.savefig(self.outputFile + "_" + IPPair[0] + "_" + IPPair[1] + "_DownloadBW" + ".png") 
            plt.show()

            upAccumulated = []
            downAccumulated = []
            maxLim = 100000
            effectDataNum = 0
            for i in range(maxLim):
                upAccumulated.append([i, 0])
                downAccumulated.append([i, 0])
            for (up, down) in zip(uploadData, downLoadData):
                if up[1]<maxLim:
                    upAccumulated[math.floor(up[1])][1] += 1
                if down[1]<maxLim:
                    downAccumulated[math.floor(down[1])][1] += 1
            
            for i in range(maxLim-1):
                upAccumulated[i+1][1] += upAccumulated[i][1]
                downAccumulated[i+1][1] += downAccumulated[i][1]


            
            plt.plot([j[0] for j in upAccumulated], [k[1]/(self.maxTime-1) for k in upAccumulated],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Uoload BW CDF")
            plt.plot([j[0] for j in downAccumulated], [k[1]/(self.maxTime-1) for k in downAccumulated],  color='red', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Download BW CDF")
            plt.xlim(0, maxLim)
            plt.xlabel('Time (s)')
            plt.ylabel('CDF')
            plt.legend()
            plt.savefig(self.outputFile + "_" + IPPair[0] + "_" + IPPair[1] + "CDF" + ".png") 
            plt.show()
                    