# tcpdump-trace-analyzer

### Utilization

Two kind of utilization 
1. Analyze RTT between desinated IP
    python3 analyze.py inputFileName outputPictureName --analyzeRTT [--IP1 192.168.1.15] [--IP2 130.211.14.80] [--storeRTT OutputDataFile]
2. Show active IP in the trace file
    python3 analyze.py inputFileName outputFileName --getIPPair [--N Threshold] [--subnet subnet]
    
    This will list all IP communication IP pair, IP interact 
    python3 analyze.py tr5_2output ./oct5_2/IP_pair.csv --getIPPair --N 300 --subnet 192.168.1

