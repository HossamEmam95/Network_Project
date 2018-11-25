import socket
import time
import os
import hashlib
import random

host = ""
port = 60000


def un_hashing(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest()


class Reciever:

    def __init__(self,win_size, timeout, filename):
        self.w = win_size
        self.completeData = ''
        self.t = timeout
        self.rec_file = ''
        self.base = 0
        self.expec_seqnum = 0
        self.last_ack_sent = -1
        self.soc = socket.socket()
        self.window = [None] * self.w
        self.active_win_packets = self.w
        self.fileclone = filename
        self.logfile = ''
        self.filepointer = 0

    def Add(self):  # check if a packet can be added to the send window
        if self.active_win_packets == 0:
            return False

        return True

    def ResponseFormat(self, seq_num, typ):
        mess_check_sum = un_hashing(str(seq_num))
        return str(mess_check_sum) + "::" + str(seq_num) + "::" + typ

    def Acknowledge(self, packet, counter):
        if counter == -1:
            self.logfile.write(str(packet.split('::')[1]) + "ready to recieve\n")
            time.sleep(1.7)
            self.soc.send(packet)
            print "Sending ack: ", str(packet.split('::')[1]) + "NAK\n"
            return
        self.last_ack_sent = int(packet.split("::")[1]) + counter
        time.sleep(1.7)
        self.soc.send(packet)
        self.logfile.write(str(packet.split('::')[1]) + "ready to recieve\n")
        print "Sending ack: ", str(packet.split('::')[1]) + "ACK"

    def remove(self, poin):
        #print self.window[0], self.window.index(str(poin))
        self.window[self.window.index(poin)] = None
        self.active_win_packets += 1

    def add(self, packet):
        pack = packet.split('::')[3]
        seqnum = int(packet.split('::')[1])
        #print packet#, self.window[seqnum % self.w]
        if self.window[seqnum % self.w] == None:
            if seqnum > self.expec_seqnum:
                self.active_win_packets -= 1
                self.window[seqnum % self.w] = packet
            elif seqnum == self.expec_seqnum:
                self.logfile.write(str(packet.split('::')[1]) + "Recieved\n")
                self.active_win_packets -= 1
                self.window[seqnum % self.w] = packet

    def appData(self):
        self.completeData += self.window[self.filepointer].split('::')[3]
        self.filepointer = self.filepointer + 1
        self.remove(self.window[self.filepointer - 1])
        if self.filepointer >= self.w:
            self.filepointer = 0

    def recieve_message(self):
        while 1:
            pack = self.soc.recv(1024)
            coun = 0
            try:
                print (pack.split('::')[1], pack.split('::')[3])
            except:
                print pack.split('::')
            if pack == 'End OF Stream':
                #print "ya"
                f = open(self.fileclone, 'wb')
                f.write(self.completeData)
                f.close()
                break
            elif int(pack.split('::')[1]) == self.expec_seqnum:
                nex = 0
                if self.Add():
                    try:
                        k = int(pack.split("::")[4])
                    except:
                        nex = 1
                    if not nex:
                        if int(pack.split("::")[4]) > 70:
                            self.add(pack)
                            packet = self.ResponseFormat(self.expec_seqnum + coun, "ACK")
                            while self.window[(int(pack.split('::')[1]) + coun) % self.w] != None:
                                self.appData()
                                coun = coun + 1
                        else:
                            packet = self.ResponseFormat(self.expec_seqnum + coun, "NAK")
                    else:
                        packet = self.ResponseFormat(self.expec_seqnum + coun, "NAK")
                    self.Acknowledge(packet, coun - 1)
                    self.expec_seqnum = self.expec_seqnum + coun
            else:
                if self.Add():
                    self.add(pack)

    def recieve(self):
        self.logfile = open(os.curdir + '/' + "reciver_log.txt", 'wb')
        self.recieve_message()
        self.logfile.close()


s = socket.socket()
s.connect((host, port))
s.send("Welcome")
mess = s.recv(1024)
args = mess.split("::")
s.close()
client = Reciever(int(args[0]), float(args[1]), args[2])
print "recieved arguments"
client.soc.connect((host, port))
client.soc.send("Welcome")
client.recieve()
client.soc.close()
