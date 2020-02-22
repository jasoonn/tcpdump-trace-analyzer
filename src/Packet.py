class Packet():
    def __init__(self, line):
        self.line = line

    def process(self):
        try:
            self.parseDate()
            self.parseSeq()
            self.parseAck()
            self.parseSend_and_RecvIP()
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
        self.sendIP = self.sender[:self.sender.rfind(".")]
        self.recvIP = self.recv[:self.recv.rfind(".")]

    #Check the pair is in the line
    def checkIP(self, IP1, IP2):
        if IP1 !=None and IP2!= None:
            if self.sendIP ==IP1 and self.recvIP == IP2:
                return True
            elif self.sendIP ==IP2 and self.recvIP == IP1:
                return True
            else:
                return False
        elif IP1 !=None:
            if self.sendIP ==IP1 or self.recvIP == IP1:
                return True
            else:
                return False
        elif IP2!=None:
            if self.sendIP ==IP2 or self.recvIP == IP2:
                return True
            else:
                return False
        else:
            return True

    #checkWhether IP1 is sender, IP2 is receiver
    def checkIPStern(self, IP1, IP2):
        if self.sendIP ==IP1 and self.recvIP == IP2:
            return True
        else:
            return False