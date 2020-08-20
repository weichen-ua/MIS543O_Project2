import sys
import getopt
import time
import random
import os
import math

import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=False):
        super(Sender, self).__init__(dest, port, filename, debug)

    def handle_response(self,response_packet):
        if Checksum.validate_checksum(response_packet):
            print("recv: %s" % response_packet)
        else:
            print("recv: %s <--- CHECKSUM FAILED" % response_packet)

    # Main sending loop.
    def start(self):
        seqno = 0
        msg = self.infile.read(500).decode()
        msg_type = None
        while not msg_type == 'end':
            next_msg = self.infile.read(500).decode()

            msg_type = 'data'
            if seqno == 0:
                msg_type = 'start'
            elif next_msg == "":
                msg_type = 'end'

            packet = self.make_packet(msg_type,seqno,msg)
            self.send(packet.encode())
            print("sent: %s" % packet)

            ##### your code goes here ... #####
            # your code should be able to handle packet 
            # 1. loss
            # 2. corruption
            # 3. duplication
            # 4. delay
            # add new functions as necessary
            response = self.receive()
            resp_str = response.decode()
            self.handle_response(resp_str)
            ##### your code ends here ... #####

            msg = next_msg
            seqno += 1

        self.infile.close()
 

'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print("BEARDOWN-TP Sender")
        print("-f FILE | --file=FILE The file to transfer; if empty reads from STDIN")
        print("-p PORT | --port=PORT The destination port, defaults to 33122")
        print("-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost")
        print("-d | --debug Print debug messages")
        print("-h | --help Print this usage message")

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:d", ["file=", "port=", "address=", "debug="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True

    s = Sender(dest,port,filename,debug)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
