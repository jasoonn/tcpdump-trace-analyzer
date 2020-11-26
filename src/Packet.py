class packet():
    def __init__(self, line):
        self.line = line

    def process(self):
        try:
            self.parseDate()
            self.parseSeq()
            self.parseAck()
            self.parseSend_and_RecvIP()
            self.len = int(self.line[self.line.rfind("length")+7:])
            return True
        except Exception as e:
            return False

    def getTime(self):
        return self.time
    
    def getSender(self,port):
        if port:
            return self.sender
        else:
            return self.sender[:self.sender.rfind(".")]

    def getRecv(self, port):
        if port:
            return self.recv
        else:
            return self.recv[:self.recv.rfind(".")]

    def getSeq(self):
        return self.seq
    
    def getAck(self):
        return self.ack

    def getLen(self):
        return self.len
            
    
    def parseDate(self):
        parse = self.line[7:22]
        while(parse[0]==' '):
            parse = parse[1:]  
        startHr = int(parse[0:2])
        startMin = int(parse[3:5])
        startSec = float(parse[6:15])
        self.time = startHr*3600 + startMin*60 + startSec

    def parseSeq(self):
        parse = self.line
        if parse.find("seq") == -1 :
            self.seq = -1
            return
        sub = parse[parse.find("seq"):]
        if (sub.find(":")>15) or (sub.find(":")==-1):
            self.seq = int(sub[4:sub.find(",")])
            return
        else:
            self.seq = int(sub[sub.find(":")+1:sub.find(",")])
            return


    def parseAck(self): 
        parse = self.line
        if parse.find(" ack") == -1:
            self.ack = -1
            return
        parse = parse[parse.find(" ack")+5:]
        self.ack = int(parse[0:parse.find(",")])
    
    def parseSend_and_RecvIP(self):
        line = self.line[self.line.find("IP")+3:]
        self.sender = line[:line.find(">")-1]
        self.recv = line[line.find(">")+2:line.find(":")]
        #Prove IP is valid
        IP = self.sender
        for i in range(4):
            int(IP[:IP.find('.')])
            if IP.find('.') == -1:
                raise("error")
            IP = IP[IP.find('.')+1:]
        int(IP)
        IP = self.recv
        for i in range(4):
            int(IP[:IP.find('.')])
            if IP.find('.') == -1:
                raise("error")
            IP = IP[IP.find('.')+1:]
        int(IP)
    

    #Check the pair is in the line
    def checkIP(self, IP1, IP2 = None):
        if IP1 !=None and IP2!= None:
            if self.sender.find(IP1) == 0 and self.recv.find(IP2) == 0:
                return True
            elif self.sender.find(IP2) == 0 and self.recv.find(IP1) == 0:
                return True
            else:
                return False
        elif IP1 !=None:
            if self.sender.find(IP1) == 0 or self.recv.find(IP1) == 0:
                return True
            else:
                return False
        elif IP2!=None:
            if self.sender.find(IP2) == 0 or self.recv.find(IP2) == 0:
                return True
            else:
                return False
        else:
            return True

if __name__ == '__main__':
    line = " 2283  16:22:22.251248 21476718us tsft -92dBm noise antenna 1 5785 MHz 11a ht/20 User 0 MCS 1 LDPC FEC 80 MHz short GI IP 192.168.1.11.51020 > 130.211.14.80.443: Flags [.], seq 4075:5443, ack 10257, win 1024, options [nop,nop,TS val 1664686985 ecr 1738227912], length 1368"
    packet = packet(line)
    packet.process()
    print(packet.getSeq())
    print(packet.checkIP("192.168.1.11", "131.211"))
