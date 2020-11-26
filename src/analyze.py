import sys
import matplotlib.pyplot as plt 
from utils import parsePacket, process_Fail, processCommand, interact, interactBool
from packet import packet
from rtt import rtt
from ipPair import ipPair
from bw import bw
from interArrival import interArrival
from packetLen import packetLen
import pickle
import numpy
from scipy.stats import pearsonr

if __name__ == '__main__':

    #Parse commands
    args = processCommand()

    #Parse data
    #  python3 analyze.py ../processedData/total_tr5 --outputFile ../result/total/cc --N 1500 --subnet 192.168.1
    #  Start 1330 finish 4500
    #  0 2 3 4 8 13
    (inputFile, faultLineNum, packets, baseTime) = parsePacket(args.inputFile, 1330, 4500)

    # Basic print packets Count
    print("Total packets count:", len(packets))
    count = 0
    for i in packets:
        if i.getSender(True).find("130.211.14.80")==0 or i.getRecv(True).find("130.211.14.80")==0:
            count += 1
    print("Poke count:", count)


    #Get IP pair information
    thisIPpair = ipPair(packets, args.outputFile, args.subnet, args.port, args.N) 
    logArr = thisIPpair.getLogArr()

    #Get analysis IP pair
    (desiredArr, labels) = interact(logArr, args.N) 
    colors = ['b', 'g', 'r', 'k', 'm', 'c', 'y']

    #Different class initialization
    #objRTT = rtt(packets, baseTime, desiredArr, args.outputFile, colors, labels)
    #objPacketLen = packetLen(packets, desiredArr, args.outputFile, colors, labels, baseTime, True)
    #objInterArrival = interArrival(packets, desiredArr, args.outputFile, colors, labels, baseTime)
    objBW = bw(packets, baseTime, desiredArr, args.outputFile, colors, labels)
    #Process RTT overall part 
    #objRTT.processServer("130.211.14.80")

    ######  Process Pokemon Go Traffic
    pokemonData = [[["192.168.1.11", "130.211.14.80"], 0, 100000], [["192.168.1.12", "130.211.14.80"], 0, 100000], [["192.168.1.14", "130.211.14.80"], 0, 100000], [["192.168.1.15", "130.211.14.80"], 0, 100000], [["192.168.1.20", "130.211.14.80"], 0, 10000], [["192.168.1.18", "130.211.14.80"], 0, 10000]]

    ###Plot Poke BW
    (pokeUploadBW, pokeDownloadBW) = objBW.processSpecificPairs(pokemonData)
    plt.plot([i/1024 for i in range(len(pokeUploadBW))], [k/pokeUploadBW[-1] for k in pokeUploadBW],  color='green', linestyle='dashed', linewidth = 1, label = "Pokemon client bandwidth")
    plt.plot([i/1024 for i in range(len(pokeDownloadBW))], [k/pokeDownloadBW[-1] for k in pokeDownloadBW],  color='red', linestyle='dashed', linewidth = 1, label = "Pokemon server bandwidth")
    plt.xlabel('Bandwidth (KBps)')
    plt.ylabel('Cumulative distribution function')
    #plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    #Plot Poke interarrival
    pokeUploadInterArr, pokeUploadPacketNum, pokeDownloadInterArr, pokeDownloadPacketNum = objInterArrival.processSpecificPairs(pokemonData)
    plt.plot([j[0] for j in pokeUploadInterArr], [k[1]/pokeUploadPacketNum for k in pokeUploadInterArr],  color='green', linestyle='dashed', linewidth = 1, label = "Pokemon client packets")
    plt.plot([j[0] for j in pokeDownloadInterArr], [k[1]/pokeDownloadPacketNum for k in pokeDownloadInterArr],  color='red', linestyle='dashed', linewidth = 1, label = "Pokemon server packets")
    #Plot inactive interarrival
    plt.xlabel('Inter-packet arrival time (s)')
    plt.ylabel('Cumulative distribution function')
    plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    #Plot Poke packetLen
    (pokeUploadPacketLen, pokeDownloadPacketLen) = objPacketLen.processSpecificPairs(pokemonData)
    plt.plot(range(len(pokeUploadPacketLen)), [k/pokeUploadPacketLen[-1] for k in pokeUploadPacketLen],  color='green', linestyle='dashed', linewidth = 1, label = "Pokemon client packets")
    plt.plot(range(len(pokeDownloadPacketLen)), [k/pokeDownloadPacketLen[-1] for k in pokeDownloadPacketLen],  color='red', linestyle='dashed', linewidth = 1, label = "Pokemon server packets")
    plt.xlabel('Packet Length (byte)')
    plt.ylabel('Cumulative distribution function')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    #Plot Poke RTT
    pokeAcc = objRTT.processSpecificPairs(pokemonData)
    plt.plot([i[0] for i in pokeAcc], [k[1] for k in pokeAcc],  color='green', linestyle='dashed', linewidth = 1, label = "Pokemon RTT")
    plt.xlabel('RTT (s)')
    plt.ylabel('Cumulative distribution function')
    plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    ######  Process active/inactive players
    activeData= [[["192.168.1.11", "130.211.14.80"], 0, 100000], [["192.168.1.12", "130.211.14.80"], 0, 100000], [["192.168.1.14", "130.211.14.80"], 0, 100000]]
    inactiveData = [[["192.168.1.15", "130.211.14.80"], 0, 100000]]

    #Plot active RTT
    activeAcc = objRTT.processSpecificPairs(activeData)
    plt.plot([i[0] for i in activeAcc], [k[1] for k in activeAcc],  color='green', linestyle='dashed', linewidth = 1, label = "Active player RTT")
    #Plot inactive RTT
    inactiveAcc = objRTT.processSpecificPairs(inactiveData)
    plt.plot([i[0] for i in inactiveAcc], [k[1] for k in inactiveAcc],  color='green', linestyle='solid', linewidth = 1, label = "Inactive player RTT")

    plt.xlabel('RTT (s)')
    plt.ylabel('Cumulative distribution function')
    plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    #Plot active packetLen
    (activeUploadPacketLen, activeDownloadPacketLen) = objPacketLen.processSpecificPairs(activeData)
    plt.plot(range(len(activeUploadPacketLen)), [k/activeUploadPacketLen[-1] for k in activeUploadPacketLen],  color='green', linestyle='dashed', linewidth = 1, label = "Active player client packets")
    plt.plot(range(len(activeDownloadPacketLen)), [k/activeDownloadPacketLen[-1] for k in activeDownloadPacketLen],  color='red', linestyle='dashed', linewidth = 1, label = "Active player server packets")
    #Plot inactive packetLen
    (inactiveUploadPacketLen, inactiveDownloadPacketLen) = objPacketLen.processSpecificPairs(inactiveData)
    plt.plot(range(len(inactiveUploadPacketLen)), [k/inactiveUploadPacketLen[-1] for k in inactiveUploadPacketLen],  color='green', linestyle='solid', linewidth = 1, label = "Inactive player client packets")
    plt.plot(range(len(inactiveDownloadPacketLen)), [k/inactiveDownloadPacketLen[-1] for k in inactiveDownloadPacketLen],  color='red', linestyle='solid', linewidth = 1, label = "Active player server packets")
    plt.xlabel('Packet Length (byte)')
    plt.ylabel('Cumulative distribution function')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    #Plot active interarrival
    activepUploadInterArr, activeUploadPacketNum, activeDownloadInterArr, activeDownloadPacketNum = objInterArrival.processSpecificPairs(activeData)
    plt.plot([j[0] for j in activepUploadInterArr], [k[1]/activeUploadPacketNum for k in activepUploadInterArr],  color='green', linestyle='dashed', linewidth = 1, label = "Active player client packets")
    plt.plot([j[0] for j in activeDownloadInterArr], [k[1]/activeDownloadPacketNum for k in activeDownloadInterArr],  color='red', linestyle='dashed', linewidth = 1, label = "Active player server packets")
    #Plot inactive interarrival
    inactiveUploadInterArr, inactiveUploadPacketNum, inactiveDownloadInterArr, inavtiveDownloadPacketNum = objInterArrival.processSpecificPairs(inactiveData)
    plt.plot([j[0] for j in inactiveUploadInterArr], [k[1]/inactiveUploadPacketNum for k in inactiveUploadInterArr],  color='green', linestyle='solid', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Inactive player client packets")
    plt.plot([j[0] for j in inactiveDownloadInterArr], [k[1]/inavtiveDownloadPacketNum for k in inactiveDownloadInterArr],  color='red', linestyle='solid', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Inactive player server packets")
    plt.xlabel('Inter-packet arrival time (s)')
    plt.ylabel('Cumulative distribution function')
    #plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()
    
    ###Plot active BW
    (activeUploadBW, activeDownloadBW) = objBW.processSpecificPairs(activeData)
    plt.plot([i/1024 for i in range(len(activeUploadBW))], [k/activeUploadBW[-1] for k in activeUploadBW],  color='green', linestyle='dashed', linewidth = 1, label = "Active player client bandwidth")
    plt.plot([i/1024 for i in range(len(activeDownloadBW))], [k/activeDownloadBW[-1] for k in activeDownloadBW],  color='red', linestyle='dashed', linewidth = 1, label = "Active player server bandwidth")
    ###Plot inactive BW
    (inactiveUploadBW, inactiveDownloadBW) = objBW.processSpecificPairs(inactiveData)
    plt.plot([i/1024 for i in range(len(inactiveUploadBW))], [k/inactiveUploadBW[-1] for k in inactiveUploadBW],  color='green', linestyle='solid', linewidth = 1, label = "Inactive player client bandwidth")
    plt.plot([i/1024 for i in range(len(inactiveDownloadBW))], [k/inactiveDownloadBW[-1] for k in inactiveDownloadBW],  color='red', linestyle='solid', linewidth = 1, label = "Inactive player server bandwidth")
    plt.xlabel('Bandwidth (KBps)')
    plt.ylabel('Cumulative distribution function')
    plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()
    

    ######  Process startup/steaty state
    startupIPData = [[["192.168.1.20", "130.211.14.80"], 850, 1080], [["192.168.1.18", "130.211.14.80"], 197, 1032]]
    steadyStateData = [[["192.168.1.11", "130.211.14.80"], 0, 100000], [["192.168.1.12", "130.211.14.80"], 0, 100000], [["192.168.1.14", "130.211.14.80"], 0, 100000], [["192.168.1.15", "130.211.14.80"], 0, 100000]]
    
    #Plot startup RTT
    startupAcc = objRTT.processSpecificPairs(startupIPData)
    plt.plot([i[0] for i in startupAcc], [k[1] for k in startupAcc],  color='green', linestyle='dashed', linewidth = 1, label = "Startup state RTT")
    #Plot steady RTT
    steadyAcc = objRTT.processSpecificPairs(steadyStateData)
    plt.plot([i[0] for i in steadyAcc], [k[1] for k in steadyAcc],  color='green', linestyle='solid', linewidth = 1, label = "Startup state RTT")

    plt.xlabel('RTT (s)')
    plt.ylabel('Cumulative distribution function')
    plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    ###Plot startup BW
    (startupUploadBW, startupDownloadBW) = objBW.processSpecificPairs(startupIPData)
    plt.plot([i/1024 for i in range(len(startupUploadBW))], [k/startupUploadBW[-1] for k in startupUploadBW],  color='green', linestyle='dashed', linewidth = 1, label = "Startup state client bandwidth")
    plt.plot([i/1024 for i in range(len(startupUploadBW))], [k/startupDownloadBW[-1] for k in startupDownloadBW],  color='red', linestyle='dashed', linewidth = 1, label = "Startup state server bandwidth")
    ###Plot steady BW
    (steadyUploadBW, steadyDownloadBW) = objBW.processSpecificPairs(steadyStateData)
    plt.plot([i/1024 for i in range(len(steadyUploadBW))], [k/steadyUploadBW[-1] for k in steadyUploadBW],  color='green', linestyle='solid', linewidth = 1, label = "Steady state client bandwidth")
    plt.plot([i/1024 for i in range(len(steadyDownloadBW))], [k/steadyDownloadBW[-1] for k in steadyDownloadBW],  color='red', linestyle='solid', linewidth = 1, label = "Steady state server bandwidth")
    plt.xlabel('Bandwidth (KBps)')
    plt.ylabel('Cumulative distribution function')
    #plt.xscale('log')
    plt.xlim(0, 150)
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    #Plot startup interarrival
    startupUploadInterArr, startupUploadPacketNum, startupDownloadInterArr, startupDownloadPacketNum = objInterArrival.processSpecificPairs(startupIPData)
    plt.plot([j[0] for j in startupUploadInterArr], [k[1]/startupUploadPacketNum for k in startupUploadInterArr],  color='green', linestyle='dashed', linewidth = 1, label = "Startup state client packets")
    plt.plot([j[0] for j in startupDownloadInterArr], [k[1]/startupDownloadPacketNum for k in startupDownloadInterArr],  color='red', linestyle='dashed', linewidth = 1, label = "Startup state server packets")
    #Plot steady interarrival
    steadyUploadInterArr, steadyupUploadPacketNum, steadyupDownloadInterArr, steadyupDownloadPacketNum = objInterArrival.processSpecificPairs(steadyStateData)
    plt.plot([j[0] for j in steadyUploadInterArr], [k[1]/steadyupUploadPacketNum for k in steadyUploadInterArr],  color='green', linestyle='solid', linewidth = 1, marker='o', markerfacecolor='blue', markersize=0.2, label = "Steady state client packets")
    plt.plot([j[0] for j in steadyupDownloadInterArr], [k[1]/steadyupDownloadPacketNum for k in steadyupDownloadInterArr],  color='red', linestyle='solid', linewidth = 1, marker='o', markerfacecolor='red', markersize=0.2, label = "Steady state server packets")
    #plt.plot([j[0] for j in steadyUploadInterArr], [k[1]/steadyupUploadPacketNum for k in steadyUploadInterArr],  color='k', linestyle='solid', linewidth = 1, label = "Steady state client packets")
    #plt.plot([j[0] for j in steadyupDownloadInterArr], [k[1]/steadyupDownloadPacketNum for k in steadyupDownloadInterArr],  color='m', linestyle='solid', linewidth = 1, label = "Steady state server packets")
    plt.xlabel('Inter-packet arrival time (s)')
    plt.ylabel('Cumulative distribution function')
    plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()

    #Plot startup packetLen
    (startupUploadPacketLen, startupDownloadPacketLen) = objPacketLen.processSpecificPairs(startupIPData)
    plt.plot(range(len(startupUploadPacketLen)), [k/startupUploadPacketLen[-1] for k in startupUploadPacketLen],  color='green', linestyle='dashed', linewidth = 1, label = "Startup state client packets")
    plt.plot(range(len(startupDownloadPacketLen)), [k/startupDownloadPacketLen[-1] for k in startupDownloadPacketLen],  color='red', linestyle='dashed', linewidth = 1, label = "Startup state server packets")
    
    #Plot steady packetLen
    (steadyUploadPacketLen, steadyDownloadPacketLen) = objPacketLen.processSpecificPairs(steadyStateData)
    plt.plot(range(len(steadyUploadPacketLen)), [k/steadyUploadPacketLen[-1] for k in steadyUploadPacketLen],  color='green', linestyle='solid', linewidth = 1, label = "Steady state client packets")
    plt.plot(range(len(steadyDownloadPacketLen)), [k/steadyDownloadPacketLen[-1] for k in steadyDownloadPacketLen],  color='red', linestyle='solid', linewidth = 1, label = "Steady state server packets")
    
    plt.xlabel('Packet Length (byte)')
    plt.ylabel('Cumulative distribution function')
    #plt.xscale('log')
    plt.legend(loc="lower right")
    plt.show()
    sys.exit()
    # for i in range(0,3500,1000):
    #     objInterArrival.getACF(i,i+1000)
    # for i in desiredArr:
    #     objInterArrival.getACF(0, 3500, clientIP=i[0])
        # for j in range(0,3500,1000):
        #     print(i)
        #     objInterArrival.getACF(j, j+1000, clientIP=i[0])


    
    #objBW.getServerBW('130.211.14.80',1)

    if interactBool("Do you want to plot specific server?"):
        interestServer = '203.104.150.4'
        interestServer = '130.211.14.80'
        if interactBool("Do you want to plot information about RTT?"):
            objRTT.getClientsTimeSeries(0, 3500, 1)
            objRTT.getServerTimeSeries(0, 3500, interestServer, 1)
            #objRTT.getOverallTimeSeries(0, 3500, 1)
        if interactBool("Do you want to plot packet len distribution?"):
            objPacketLen.plotSpecificServer(packets, interestServer)
        if interactBool("Do you want to plot inter-arrival time?"):
            objInterArrival.plotSpecificServer(packets, interestServer)
        if interactBool("Do you want to plot information about Bandwith?"):
            objBW.plotSpecificServer(packets, interestServer, 10)

    if interactBool("Do you want to plot individuals?"):
        if interactBool("Do you want to plot information about RTT?"):
            objRTT.plotRTT()
            objRTT.plotRTTDistribution()
        if interactBool("Do you want to plot packet len distribution?"):
            objPacketLen.plotDivide()
        if interactBool("Do you want to plot inter-arrival time?"):
            objInterArrival.plotDivide()
        if interactBool("Do you want to plot information about Bandwith?"):
            objBW.plotDivide()

    if interactBool("Do you want to plot all pairs on the same plot?"):
        if interactBool("Do you want to plot information about RTT?"):
            objRTT.plotTimeSeries(0, 500, 10)
            objRTT.plotTimeSeries(500, 1000,10)
            objRTT.plotTimeSeries(1000, 1500, 10)
            objRTT.plotTimeSeries(1500, 2000, 10)
            objRTT.plotTimeSeries(2000, 2500, 10)
            objRTT.plotTimeSeries(2500, 3000, 10)
            objRTT.plotTimeSeries(3000, 3500, 10)
            #objRTT.plotRTTDistribution()
        if interactBool("Do you want to plot packet len distribution?"):
            #objPacketLen.plotTogether()
            objPacketLen.plotTimeSeries(0, 500, 10)
            objPacketLen.plotTimeSeries(500, 1000, 10)
            objPacketLen.plotTimeSeries(1000, 1500, 10)
            objPacketLen.plotTimeSeries(1500, 2000, 10)
            objPacketLen.plotTimeSeries(2000, 2500, 10)
            objPacketLen.plotTimeSeries(2500, 3000, 10)
            objPacketLen.plotTimeSeries(3000, 3500, 10)
        if interactBool("Do you want to plot inter-arrival time?"):
            objInterArrival.plotTimeSeries(0, 500, 10)
            objInterArrival.plotTimeSeries(500, 1000, 10)
            objInterArrival.plotTimeSeries(1000, 1500, 10)
            objInterArrival.plotTimeSeries(1500, 2000, 10)
            objInterArrival.plotTimeSeries(2000, 2500, 10)
            objInterArrival.plotTimeSeries(2500, 3000, 10)
            objInterArrival.plotTimeSeries(3000, 3500, 10)
            #objInterArrival.plotTogether()
        if interactBool("Do you want to plot information about Bandwith?"):
            objBW.plotTimeSeries(0, 500, 10)
            objBW.plotTimeSeries(500, 1000, 10)
            objBW.plotTimeSeries(1000, 1500, 10)
            objBW.plotTimeSeries(1500, 2500, 10)
            objBW.plotTimeSeries(2000, 2500, 10)
            objBW.plotTimeSeries(2500, 3000, 10)
            objBW.plotTimeSeries(3000, 3500, 10)
            #objBW.plotTogether()    


    # RTT and BW correlation
    # rttTimes = objRTT.getClientsTimeSeries(0, 3500, 1)
    # (uploadBW, downloadBW) = objBW.getOverallBW(1)
    # print("client to overall")
    # for i in range(len(labels)):
    #     labels[i] = labels[i] + "1s"

    # upperbound = 1
    # for index, rtt in enumerate(rttTimes):
    #     effectiveUploadPair = []
    #     effectiveDownloadPair = []
    #     effectiveOverall = []
    #     #Deal with overall
    #     for j in range(objBW.arrLen):
    #         if rtt[j][1] != 0 and rtt[j][1]<upperbound:
    #             effectiveUploadPair.append([uploadBW[j][1], rtt[j][1]])
    #             effectiveDownloadPair.append([downloadBW[j][1], rtt[j][1]])
    #             effectiveOverall.append([uploadBW[j][1]+downloadBW[j][1], rtt[j][1]]) 

    #     npRTT = numpy.array([j[1] for j in effectiveUploadPair])
    #     npUpBW = numpy.array([j[0] for j in effectiveUploadPair])
    #     npDownBW = numpy.array([j[0] for j in effectiveDownloadPair])
    #     npOverallBW = numpy.array([j[0] for j in effectiveOverall])

    #     #print("col", pearsonr(npUpBW, npRTT))

    #     plt.scatter(npRTT, npUpBW, label='Pearson’s Correlation:' + str((numpy.cov(npUpBW, npRTT)[0][1]/(numpy.std(npUpBW)*numpy.std(npRTT)))))
    #     plt.legend()
    #     plt.savefig(args.outputFile + "_" + labels[index] + "_" + "_allUP" + ".png")
    #     plt.show()
    #     print("mean", numpy.mean(npUpBW), 'std', numpy.std(npUpBW), 'cov', numpy.cov(npUpBW, npRTT))

    #     plt.scatter(npRTT, npDownBW, label='Pearson’s Correlation:' + str(numpy.cov(npDownBW, npRTT)[0][1]/(numpy.std(npDownBW)*numpy.std(npRTT))))
    #     plt.legend()
    #     plt.savefig(args.outputFile + "_" + labels[index] + "_" + "_allDOWN" + ".png")
    #     plt.show()
    #     print("mean", numpy.mean(npDownBW), 'std', numpy.std(npDownBW), 'cov', numpy.cov(npDownBW, npRTT))

    #     plt.scatter(npRTT, npOverallBW, label='Pearson’s Correlation:' + str(numpy.cov(npOverallBW, npRTT)[0][1]/(numpy.std(npOverallBW)*numpy.std(npRTT))))
    #     plt.legend()
    #     plt.savefig(args.outputFile + "_" + labels[index] + "_" + "_allBOTH" + ".png")
    #     plt.show()
        
    #     print("mean", numpy.mean(npOverallBW), 'std', numpy.std(npOverallBW))

    # print("Client to client")
    # (clientsUpBW, clientsDownBW) = objBW.getClientsBW(1)
    # index = 0
    # for label, upBW, downBW, rttTime in zip(labels, clientsUpBW, clientsDownBW, rttTimes):
    #     effectiveUploadPair = []
    #     effectiveDownloadPair = []
    #     effectiveOverall = []
    #     for j in range(objBW.arrLen):
    #         if rtt[j][1] != 0 and rtt[j][1]<upperbound:
    #             effectiveUploadPair.append([upBW[j][1], rtt[j][1]])
    #             effectiveDownloadPair.append([downBW[j][1], rtt[j][1]])
    #             effectiveOverall.append([upBW[j][1]+downBW[j][1], rtt[j][1]]) 
        
    #     npRTT = numpy.array([j[1] for j in effectiveUploadPair])
    #     npUpBW = numpy.array([j[0] for j in effectiveUploadPair])
    #     npDownBW = numpy.array([j[0] for j in effectiveDownloadPair])
    #     npOverallBW = numpy.array([j[0] for j in effectiveOverall])

    #     plt.scatter(npRTT, npUpBW, label='Pearson’s Correlation:' + str((numpy.cov(npUpBW, npRTT)[0][1]/(numpy.std(npUpBW)*numpy.std(npRTT)))))
    #     plt.legend()
    #     plt.savefig(args.outputFile + "_" + labels[index] + "_" + "_clientUP" + ".png")
    #     plt.show()
    #     print("mean", numpy.mean(npUpBW), 'std', numpy.std(npUpBW), 'cov', numpy.cov(npUpBW, npRTT))

    #     plt.scatter(npRTT, npDownBW, label='Pearson’s Correlation:' + str((numpy.cov(npDownBW, npRTT)[0][1]/(numpy.std(npDownBW)*numpy.std(npRTT)))))
    #     plt.legend()
    #     plt.savefig(args.outputFile + "_" + labels[index] + "_" + "_clientDOWN" + ".png")
    #     plt.show()
    #     print("mean", numpy.mean(npDownBW), 'std', numpy.std(npDownBW), 'cov', numpy.cov(npDownBW, npRTT))

    #     plt.scatter(npRTT, npOverallBW, label='Pearson’s Correlation:' + str((numpy.cov(npOverallBW, npRTT)[0][1]/(numpy.std(npOverallBW)*numpy.std(npRTT)))))
    #     plt.legend()
    #     plt.savefig(args.outputFile + "_" + labels[index] + "_" + "_clientBOTH" + ".png")
    #     plt.show()
    #     print("mean", numpy.mean(npOverallBW), 'std', numpy.std(npOverallBW))
    #     index+=1

    #Finish write IP pair  
    thisIPpair.close()   

    #Print fail number
    if args.printFault:
        for index, i in enumerate(process_Fail(faultLineNum)):
            print(index+1, i)
    inputFile.close()
