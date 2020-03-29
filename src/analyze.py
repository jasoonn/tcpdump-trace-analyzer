import sys
import matplotlib.pyplot as plt 
from utils import parsePacket, process_Fail, processCommand, interact, getMaxTime, interactBool, plotInterArrival
from Packet import Packet
from rtt import  getRTT, plotRTT, plotRTTDistribution
from ipPair import ipPair
from bw import bw
import pickle

if __name__ == '__main__':

    #Parse commands
    args = processCommand()

    #Parse data
    (inputFile, faultLineNum, Packets, baseTime) = parsePacket(args.inputFile)

    #Get IP pair information
    thisIPpair = ipPair(Packets, args.outputFile, args.subnet, args.port, args.N) 
    logArr = thisIPpair.getLogArr()

    #Get analysis IP pair
    (desiredArr, labels) = interact(logArr, args.N) 

    #To see whether plot inter-arrival time
    if interactBool("Do you want to plot inter-arrival time?"):
        plotInterArrival(Packets, desiredArr, args.outputFile)

    #To see whether plot RTT
    if interactBool("Do you want to plot information about RTT?"):
        datas = getRTT(Packets, baseTime, desiredArr, args.outputFile)
        maxtime = getMaxTime(datas)
        plotRTT(datas, labels, maxtime, args.outputFile)
        plotRTTDistribution(datas, labels, args.outputFile)

    #To see whether plot BandWidth
    if interactBool("Do you want to plot information about Bandwith?"):
        BW = bw(Packets, baseTime, desiredArr, args.outputFile)
        BW.plotDivide()

    

    #Finish write IP pair  
    thisIPpair.close()   

    #Print fail number
    if args.printFault:
        for index, i in enumerate(process_Fail(faultLineNum)):
            print(index+1, i)
    inputFile.close()
