from Packet import Packet
import matplotlib.pyplot as plt

def getRTT(packets, baseTime, desiredArr, outputFile):
    datas = []
    for IPPair in desiredArr:
        possible = []
        data = []
        for i, packet in enumerate(packets):
            if (i%200 ==0):
                print([IPPair ,i], end="\r", flush=True)
            if packet.checkIP(IPPair[0], IPPair[1])==False:
                continue
            if packet.getSeq() != -1:
                possible.append(packet)
            if packet.getAck() != -1:
                for j, pair in enumerate(possible):
                    if pair.getSeq() == packet.getAck():
                        if packet.getRecv(True) == pair.getSender(True) and packet.getSender(True) == pair.getRecv(True):
                            data.append([pair.getTime()-baseTime, packet.getTime()-pair.getTime()])
                            possible.pop(j)
        datas.append(data)
        # data = sorted(data, key=cmp_to_key(firstCompare))
        # plt.plot([j[0] for j in data], [k[1] for k in data],  color='green', linestyle='dashed', linewidth = 1, marker='o', markerfacecolor='blue', markersize=3)
        # plt.suptitle(IPPair[0] + "_" + IPPair[1], fontsize=16)
        # plt.xlim(0,getMaxTime(datas))
        # plt.xlabel('Time (s)')
        # plt.ylabel('RTT (s)') 
        # plt.savefig(outputFile + "_" + IPPair[0] + "_" + IPPair[1] + ".png")
        # plt.show()
        # print(len(data))
    return datas

def plotRTT(datas, labels, maxTime, outputFile, startTime = 0):
    colors = ['b', 'g', 'r', 'k', 'm', 'c', 'y']
    for index, data in enumerate(datas):
        col = colors[index]
        plt.scatter([j[0] for j in data], [k[1] for k in data], s=2, color = col, label = labels[index])
    plt.legend()
    plt.xlim(startTime, maxTime)
    #plt.ylim(startTime, 0.25)
    plt.xlabel('Time (s)')
    plt.ylabel('RTT (s)') 
    plt.savefig(outputFile + "RTT.png")
    plt.show()

def plotRTTDistribution(datas, labels, outputFile, longTime = 100, startTime=0):
    colors = ['b', 'g', 'r', 'k', 'm', 'c', 'y']
    #Second, plot PDF
    allOver = []
    allAccumulated = []
    for index, data in enumerate(datas):
        effectDataNum = 0
        over = []
        accumulated = []
        for i in [x*0.001 for x in range(int(int(longTime)*1000))]:
            accumulated.append([i, 0])
        for i in data:
            if i[0]>=int(startTime):
                if i[1]>int(longTime):
                    over.append(i[1])
                    continue
                accumulated[int(i[1]*1000)][1]+=1
                effectDataNum +=1
        for i in range(len(accumulated)):
            accumulated[i][1] /= effectDataNum
        allAccumulated.append(accumulated)
        allOver.append(over)
        max = 0
        for i in over:
            if i>max:
                max=i
        print(index, max)
        plt.scatter([j[0]+0.001 for j in accumulated], [k[1] for k in accumulated], s=0.5, color = colors[index], label = labels[index])
    plt.legend()
    plt.xscale('log')
    plt.xlabel('RTT Time (s)')
    plt.ylabel('PDF')
    plt.savefig(outputFile + "PDF.png")
    plt.show()

    plt.xscale('log')
    for index, data in enumerate(datas):
        for i in range(len(allAccumulated[index])-1):
            allAccumulated[index][i+1][1] += allAccumulated[index][i][1]
        plt.scatter([j[0]+0.0001 for j in allAccumulated[index]], [k[1] for k in allAccumulated[index]], s=1, color = colors[index], label = labels[index])
    plt.legend()
    plt.xlabel('RTT Time (s)')
    plt.ylabel('CDF') 
    plt.savefig(outputFile + "CDF.png")
    plt.show()
