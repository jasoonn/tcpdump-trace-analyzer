from Packet import Packet

a = "14233  16:24:00.066648 503677121us tsft -38dBm signal -92dBm noise antenna 1 5785 MHz 11a ht/20 [|802.11]IP 104.66.139.232.443 > 192.168.1.15.63387: Flags [.], seq 201200:202648, ack 1344, win 260, options [nop,nop,TS val 345384272 ecr 1171809886], length 1448"
b = Packet(a)
print(b.process())
