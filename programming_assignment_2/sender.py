import socket
import time
import os
import hashlib
import random

host = ""
port = 60000


def hashing(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest()


class Sender:

    def __init__(self, win_size, timeout, num_packets, nak_num):
        self.w = win_size
        self.t = timeout
        self.n = num_packets
        self.filename = "input.txt"
        self.cur_seq = 0
        self.active_spaces = self.w
        self.window = win_size * [None]
        self.soc = socket.socket()
        self.last_sent_seqnum = -1
        self.last_ack_seqnum = -1
        self.logfile = ''
        self.flag = 0
        self.nak_num = nak_num


    def canAdd(self):  # check if a packet can be added to the send window
        if self.active_spaces == 0:
            return False
        else:
            return True

    def sendPack(self, pack):  # function to send the packet through the socket
        time.sleep(1.5)
        conn.send(pack)
        print "Sending packet No.", int(pack.split('::')[1])
        self.logfile.write(str(pack.split('::')[1]) + " Sending\n")

    def add(self, pack):  # add a packet to the send window
        self.last_sent_seqnum = self.cur_seq
        self.cur_seq += 1
        self.window[self.w - self.active_spaces] = pack
        self.active_spaces -= 1
        self.sendPack(pack)


    def work(self):  # work this to send packets from the file
        try:
            fil = open(self.filename, 'rb')
            data = fil.read()
            data = data.strip()
            pack_list = self.form_pack(data, 7)
            fil.close()
        except IOError:
            print "No such file exists"
        fname="servlog.txt"
        self.logfile=open(os.curdir + "/" + fname, "w+")
        l=len(pack_list)
        self.sendmess(pack_list, l)

    def resend(self):  # function to resend packet if lost
        cur_num = 0
        # while cur_num < self.w - self.active_spaces:
        print "Resending: ", str(self.window[cur_num].split('::')[1])
        self.logfile.write(str(self.window[cur_num].split('::')[1]) + " Re-sending\n")
        time.sleep(1.4)
        temp = self.window[cur_num].split('::')
        self.window[cur_num] = temp[0] + '::' + temp[1] + '::' + temp[2] + '::' + temp[3] + '::' + str(random.randint(70,100))
        print self.window[cur_num].split('::')[1], self.window[cur_num].split('::')[3]

        conn.send(self.window[cur_num])
        cur_num += 1

    def makePack(self, num, pac):  # Create a packet
        sequence_number = num
        file_check_sum = hashing(pac)
        pack_size = len(pac)
        prob = random.randint(0, 100)
        packet = str(file_check_sum) + '::' + str(sequence_number) + \
                     '::' + str(pack_size) + '::' + \
                                   str(pac) + '::' + str('90')
        if self.nak_num == sequence_number:
            self.nak_num = 111111111
            packet = str(file_check_sum) + '::' + str(sequence_number) + \
                         '::' + str(pack_size) + '::' + \
                                       str(pac) + '::' + str('50')
        return packet

    def form_pack(self, data, num):  # create packets from datas
        lis = []
        while data:
            lis.append(data[:num])
            data = data[num:]
        return lis

    def acc_Acks(self):  # check if all the sent packets have been ACKed
        try:
            packet = conn.recv(1024)
            self.logfile.write("recieved: " + str(packet.split("::")[-2]) + " :: " + str(packet.split("::")[-1]) + "\n")
        except:
            print 'Connection lost due to timeout!'
            self.logfile.write(time.ctime(time.time()) + "\t" + str(self.last_ack_seqnum + 1) + "Lost TImeout")
            return 0
        if packet.split('::')[2] == "NAK":
            return 0
        print "Recieved Ack number: ", packet.split('::')[1]
        if int(packet.split('::')[1]) == self.last_ack_seqnum + 1:
            self.last_ack_seqnum = int(packet.split('::')[1])
            self.window.pop(0)
            self.window.append(None)
            self.active_spaces += 1
            return 1

        elif int(packet.split('::')[1]) > self.last_ack_seqnum + 1:
            k = self.last_ack_seqnum
            while(k < int(packet.split('::')[1])):
                self.window.pop(0)
                self.window.append(None)
                self.active_spaces += 1
                k = k + 1
            self.last_ack_seqnum = int(packet.split('::')[1])
            return 1

        else:
            return 0

    def sendmess(self, pack_list, length):  # send the messages till all packets are sent
        cur_pack = 0
        while (cur_pack < length or self.last_ack_seqnum != length - 1):
            #print "hjff"
            while self.canAdd() and cur_pack != length:
                pack = self.makePack(cur_pack, pack_list[cur_pack])
                cur_pack = cur_pack + 1
                print pack.split('::')[1], pack.split('::')[3]
                self.add(pack)
            print "\n"
            #print "wwaaaaattt"
            if self.acc_Acks() == 0:
                time.sleep(1)
                self.resend()
        print "END"
        time.sleep(1)
        conn.send("End OF Stream")





win = 4
numpac = 8
tim = 1
# non_ack = raw_input("enter the packet number you want to send non awk on it: ")
non_ack = 3
server=Sender(int(win), float(tim), int(numpac), int(non_ack))
server.soc.bind((host, port))
server.soc.listen(8000)
conn, addr=server.soc.accept()
data = conn.recv(1024)
print "recieved connection"
conn.send(str(win) + "::" + str(tim) + "::" + "output.txt")
conn.close()
server.soc.settimeout(5)
conn, addr = server.soc.accept()
data = conn.recv(1024)
server.work()
conn.close()
