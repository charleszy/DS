'''
Created on Apr 2, 2013

@author: Coco
'''
import wx
from application import *
from game import *
import threading
import time

class StartPage(wx.Frame):

    def __init__(self, userlist, parent, id):
        wx.Frame.__init__(self, parent, id, "Zatacka", size=(1000, 800))
        global panel
        panel = wx.Panel(self)
        
        custom = wx.StaticText(panel, -1, "Welcome to Zatacka!", (10, 30), (500, -1), wx.ALIGN_CENTER)
        custom.SetForegroundColour('white')
        custom.SetBackgroundColour('blue')
        
        try:
            image_file = 'ZatackaLogo.png'
            img = wx.Image(image_file, wx.BITMAP_TYPE_ANY)
#            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            
        except IOError:
            print "Image not found"
        
        startButton=wx.Button(panel, label="Start", pos=(400,100),size=(150,100))
        self.Bind(wx.EVT_BUTTON, self.startGame, startButton)
        
        receiveButton=wx.Button(panel, label="Receive", pos=(600,100),size=(150,100))
        receiveButton.Bind(wx.EVT_BUTTON, self.receive)
        
        self.playerList = PlayerList(parent=None, id=-1)

    def startGame(self, event):
        print "start"
        p1.main_func("1")
        
    def receive(self, event):
        print "receive"
        p1.main_func("2")
#        self.playerList = PlayerList(parent=None, id=-1)
        while p1.peerlist is None:
            pass
        self.playerList.Show()
        self.playerList.Refresh()

class PlayerList(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Ready Players', size=(800, 800))
        panel = wx.Panel(self)
        
        self.userlistbox = wx.ListBox(panel, -1, (100,100), (400,500), p1.peerlist)
        self.oldlist = []
        
    def refreshList(self, newUserlist):
        print "enter refresh"
        if self.oldlist != p1.peerlist:
            self.userlistbox.Set(p1.peerlist)
            self.oldlist = p1.peerlist

class newPlayer(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'New Player', size=(400, 120))
        panel=wx.Panel(self)
        
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, -1, 'Name')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        self.tc = wx.TextCtrl(panel, -1)
        
        hbox1.Add(self.tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        vbox.Add((-1, 10))
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='OK', size=(70, 30))
        btn1.Bind(wx.EVT_BUTTON, self.createPlayer)
        hbox2.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.closebutton, btn2)

        hbox2.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)
        
    def createPlayer(self, event):
        print "create"
        txt = self.tc.GetValue()
        print txt
        p1.setName(txt)
        self.Close(True)
        custom1 = wx.StaticText(panel, -1, txt, (20, 100), (500, -1), wx.ALIGN_CENTER)
        
    def closebutton(self, event):
        self.Close(True)

class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            print "refresh"
            startFrame.playerList.refreshList(t.getPlayerNames())
            self.event.wait( 1 )

    def stop(self):
        self.event.set()
               
if __name__=='__main__':
    app = wx.PySimpleApp()
    p1 = Player()
    p1.setName('CharlesZY')

    t = Table('table1', p1)
#    t.printPlayer();
    t.addPlayer(p1)
#    t.printPlayer();
    s = Server(123457)
    s.addTable(t)
    userlist = t.getPlayerNames()
    print userlist
    startFrame = StartPage(userlist, parent=None, id=-1)
    startFrame.Show()
    t.addPlayer(p1)
    newPlayerFrame = newPlayer(parent=None, id=1)
    newPlayerFrame.Show()
    
#    tmr = TimerClass()
#    tmr.start()
#
#    time.sleep( 20 )
#    tmr.stop()
    
#    startFrame.playerList.refreshList(t.getPlayerNames())
    app.MainLoop()
    