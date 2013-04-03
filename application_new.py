import socket
import logging
import time
import pickle
import threading 
 
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )
global peerlist
global myport
global myip
peerlist = []
BC_PORT = 12345
myport = 1236
myip = socket.gethostbyname(socket.gethostname())

class Message ():
    def __init__(self, data, msg_type):
        self.data = data
        self.msg_type = msg_type
        
    def get_message(self):
        return self
            

class Handler ( threading.Thread ):
    
    def __init__ (self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        
    def run (self ):
        while True : 
            client_msg = self.conn.recv(1024)
            message = client_msg
            if message != '':
                print 'Received data  :', message
            #print "Received data: %s" % repr(message.msg)

class server( threading.Thread ):
    def __init__(self, port, choice):
        threading.Thread.__init__(self)
        self.port = port
        self.creator = choice

    def run ( self ):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))    
        s.listen(5)

        if (self.creator == 1):
            while True :
                conn, addr = s.accept()
                print 'Accepted connection from '
                print addr
                handler = Handler(conn,addr)
                handler.start()
        else :
            conn, addr = s.accept()
            print 'Accepted connection from '
            print addr
            client_resp = conn.recv(1024)
            list_of_players = pickle.loads(client_resp)
            #print 'Received data  :', list_of_players
            #print 'Received data  :', message.data
            peerlist = list_of_players
            print 'List : ', peerlist
            for j in range(0,len(peerlist)) :
                    (peer_addr,peer_port) = peerlist[j]
                    if (peer_port != myport):
                        client_thread = client(peer_addr, peer_port, "hi") 
                        client_thread.start()
            while True :
                conn, addr = s.accept()
                print 'Accepted connection from '
                print addr
                handler = Handler(conn,addr)
                handler.start()

class client(threading.Thread):
    def __init__(self, ip, port, data):
        threading.Thread.__init__(self)
        self.port = port
        self.host = ip # Get local machine name
        self.data = data
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
    def run(self):
        print 'Connecting to ', self.host, self.port
        self.clientSock.connect((self.host, self.port))      
        send_data  = pickle.dumps(self.data)
        self.clientSock.send(send_data)
        #while True:
         #   msg = raw_input('Client : ')
          #  self.clientSock.send(msg)

class Player():
    
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
            choice = raw_input("1.Send Broadcast 2.Wait for Broadcast \nChoice???")    
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
                print 'Sender Port ', sender_port
                print 'Sender IP ', sender_ip
                sender_address = (sender_ip, int(sender_port))
                server_socket.sendto("join", sender_address)
                print "Sent join"
                sock.close()
            
        server_socket.close()
        
        #start the server thread  
        server_thread =  server(myport, int(choice))   
        server_thread.start()

        #start client threads for all the players who responded
        if (choice == "1"):
            num_other_players = len(peerlist)
            send_list = peerlist
            send_list.append(address)
            print peerlist
            for i in range(0,num_other_players) :
                (peer_addr,peer_port) = peerlist[i]
                client_thread = client(peer_addr, peer_port, send_list) 
                client_thread.start()
                
                
                
