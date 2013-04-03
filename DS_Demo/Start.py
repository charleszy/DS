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
        panel = wx.Panel(self)
        
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
    userlist = t.getPlayerNames()
    print userlist
    startFrame = StartPage(userlist, parent=None, id=-1)
    startFrame.Show()
    app.MainLoop()
    