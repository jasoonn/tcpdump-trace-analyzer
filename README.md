# tcpdump-trace-analyzer

This is only used for analyzing TCP packet.
### How to get raw data and processedData?
Step1: Taking your own trace(Ubuntu):
``` 
    tcpdump -w [output filename]
    Press control-c to stop recording.
```
Step2: Firlter trace file
```
    tcpdump -r [input trace filename] --number -n 'tcp' > [output filename]
```

```
### Utilization

Two kind of utilization 
1. Analyze RTT between desinated IP
    python3 analyze.py inputFileName outputPictureName --analyzeRTT [--IP1 192.168.1.15] [--IP2 130.211.14.80] [--storeRTT OutputDataFile]
2. Show active IP in the trace file
    python3 analyze.py inputFileName outputFileName --getIPPair [--N Threshold] [--subnet subnet]
    
    This will list all IP communication IP pair, IP interact 
    python3 analyze.py tr5_2output ./oct5_2/IP_pair.csv --getIPPair --N 300 --subnet 192.168.1

python3 analyze.py ../processedData/total_tr5 --outputFile ../result/total/cc --N 1500 --subnet 192.168.1
