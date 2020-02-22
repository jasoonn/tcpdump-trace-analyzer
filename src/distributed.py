import pickle
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
from argparse import ArgumentParser
from utils import parseLog
import math

#Parse args
def processCommand():
    parser = ArgumentParser()
    parser.add_argument('inputFile', help='Input filename')
    parser.add_argument('outputFile', help='Input filename')
    parser.add_argument('--startTime', default=0, help='Ploting start time')
    parser.add_argument('--endTime', default=-1, help='Ploting end time')
    parser.add_argument('--longTime', default=1, help='Ploting end time')
    return parser.parse_args()

if __name__ == '__main__':
    args = processCommand()
    print(args)
    files = parseLog(args.inputFile)
    datas = []
    #Load Data
    for i in files:
        with open(i, "rb") as fp:
            datas.append(pickle.load(fp))
    #Find Max Time
    if args.endTime==-1:
        max = -1
        for data in datas:
            if data[-1][0]>max:
                max = data[-1][0]    
        args.endTime = max*1.01
        print("Default max time:",max)
    #Basic Color Setting
    colors = ['b', 'g', 'r', 'k', 'm', 'c', 'y']

    #First, Plot RTT scalars
    for index, data in enumerate(datas):
        if len(datas)> len(colors):
            col = cm.rainbow(index/len(datas))
        else:
            col = colors[index]
        plt.scatter([j[0] for j in data], [k[1] for k in data], s=2, color = col, label = files[index])
    plt.legend()
    plt.xlim(int(args.startTime), int(args.endTime))
    plt.xlabel('Time (s)')
    plt.ylabel('RTT (s)') 
    plt.savefig(args.outputFile + "RTT.png")
    plt.show()
    

    #Second, plot PDF
    allOver = []
    allAccumulated = []
    for index, data in enumerate(datas):
        effectDataNum = 0
        over = []
        accumulated = []
        for i in [x*0.001 for x in range(int(int(args.longTime)*1000))]:
            accumulated.append([i, 0])
        for i in data:
            if i[0]>=int(args.startTime):
                if i[1]>int(args.longTime):
                    over.append(i[1])
                    continue
                accumulated[int(i[1]*1000)][1]+=1
                effectDataNum +=1
        if len(datas)> len(colors):
            col = cm.rainbow(index/len(datas))
        else:
            col = colors[index]
        for i in range(len(accumulated)):
            accumulated[i][1] /= effectDataNum
        allAccumulated.append(accumulated)
        allOver.append(over)
        max = 0
        for i in over:
            if i>max:
                max=i
        print(index, max)
        plt.scatter([j[0]+0.001 for j in accumulated], [k[1] for k in accumulated], s=0.5, color = col, label = files[index])
    plt.legend()
    plt.xscale('log')
    plt.xlabel('RTT Time (s)')
    plt.ylabel('PDF')
    plt.savefig(args.outputFile + "PDF.png")
    plt.show()
    

    #Third, plot CDF
    plt.xscale('log')
    for index, data in enumerate(datas):
        for i in range(len(allAccumulated[index])-1):
            allAccumulated[index][i+1][1] += allAccumulated[index][i][1]
        if len(datas)> len(colors):
            col = cm.rainbow(index/len(datas))
        else:
            col = colors[index]
        plt.scatter([j[0]+0.001 for j in allAccumulated[index]], [k[1] for k in allAccumulated[index]], s=1, color = col, label = files[index])
    plt.legend()
    plt.xlabel('RTT Time (s)')
    plt.ylabel('CDF') 
    plt.savefig(args.outputFile + "CDF.png")
    plt.show()
    



