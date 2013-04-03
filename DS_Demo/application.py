import socket
import logging
import time
import pickle
import threading 
 
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

class Handler ( threading.Thread ):
    
    def __init__ (self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        
    def run (self ):
        while True : 
            msg = self.conn.recv(1024)
            print "Received data: %s" % repr(msg)

class server( threading.Thread ):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port

    def run ( self ):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))    
        s.listen(5)
        while True :
            conn, addr = s.accept()
            print 'Accepted connection from '
            print addr
            handler = Handler(conn,addr)
            handler.start()

class client(threading.Thread):
    def __init__(self, ip, port, data, is_list):
        threading.Thread.__init__(self)
        self.port = port
        self.host = ip # Get local machine name
        self.data = data
        self.is_list = is_list
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
    def run(self):
        print 'Connecting to ', self.host, self.port
        self.clientSock.connect((self.host, self.port))      
        print "Sending list to client"
        #if (self.isList == 1):
            #send_data  = pickle.dumps(self.data)
            #self.clientSock.send(send_data)
        #else :
        while True:
            msg = raw_input('Client : ')
            self.clientSock.send(msg)

class Player():
   
    global peerlist
    peerlist = []
    BC_PORT = 12345
    global myport
    myport = 1234
    
    global myip
    myip = socket.gethostbyname(socket.gethostname())
    address = (myip, myport)
    
    def __init__(self):
        self.logger = logging.getLogger('Player')
        self.logger.debug('__init__')
   
    if __name__ == '__main__':

        logger = logging.getLogger('Player')

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(address)
        server_socket.setblocking(False)
        flag = True
        
        # User Prompt initially
        while flag:
#            choice = raw_input("1.Send Broadcast 2.Wait for Broadcast \nChoice???")
            logger.debug('Choice1: "%s"', choice)
    
            if (choice == "1"):
                flag = False
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(('', 0))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
             
                myaddr = (myip,myport)
                broadcastdata  = pickle.dumps(myaddr)
                while (len(peerlist) < 1):
                    begin = time.time()
    
                    while ((time.time() - begin) < 10) :
                        sock.sendto(broadcastdata, ('<broadcast>', BC_PORT))
                        #print "Broadcast message sent"
                        try :
                            recv_data, addr = server_socket.recvfrom(2048)
                            peerlist.append(addr)
                            print peerlist
                        except: 
                            pass
                
                sock.close()
    
            if (choice == "2"):
                # Receive a response
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind(('', BC_PORT))
                sock.setblocking(False)
                begin = time.time()
    
                while ((time.time() - begin) < 10) :
                    try :
                        message, addr = sock.recvfrom(8192)
                        flag = False
                        break
                    except:
                        pass
                (sender_ip,sender_port) = pickle.loads(message)
                print 'Sender Port '
                print sender_port
                print 'Sender IP ' 
                print sender_ip
                sender_address = (sender_ip, int(sender_port))
                print sender_address
                server_socket.sendto("join", sender_address)
                print "Sent join"
                sock.close()
            
        server_socket.close()
        
        #start the server thread  
        server_thread =  server(myport)   
        server_thread.start()

        #start client threads for all the players who responded
        if (choice == "1"):
            num_other_players = len(peerlist)
            send_list = peerlist
            send_list.append(address)
            print peerlist
            for i in range(0,num_other_players) :
                (peer_addr,peer_port) = peerlist[i]
                client_thread = client(peer_addr, peer_port, send_list, 1) 
                client_thread.start()
                
        elif (choice == "2"):
            while True:
                if(len(peerlist) != 0):
                    break
                
            for j in range(0,len(peerlist)) :
                if (peer_port != myport):
                    (peer_addr,peer_port) = peerlist[i]
                    client_thread = client(peer_addr, peer_port, send_list, 1) 
                    client_thread.start()
        
                
