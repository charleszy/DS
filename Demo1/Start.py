'''
Created on Apr 2, 2013

@author: Coco
'''
import wx
from game import *
import threading
import time

class StartPage(wx.Frame):

    def __init__(self, userlist, parent, id):
        wx.Frame.__init__(self, parent, id, "Zatacka", size=(1000, 800))
        global panel
        panel = wx.Panel(self)
        
        zatacka = wx.StaticText(panel, -1, " welcome to Zatacka!", (440, 80), (450, 150), wx.ALIGN_CENTER)
        global font
        font = wx.Font(28, wx.DECORATIVE, -1, wx.ITALIC, wx.NORMAL)
        zatacka.SetFont(font)

        img = wx.EmptyImage(240,240)
        self.imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(img), (400, 250))
 
        try:
            image_file = 'ZatackaLogo.png'
            img = wx.Image(image_file, wx.BITMAP_TYPE_ANY)
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        except IOError:
            print "Image not found"
        
        startButton=wx.Button(panel, label="Start Game", pos=(300,100),size=(200,100))
        self.Bind(wx.EVT_BUTTON, self.startGame, startButton)
        
        self.receiveButton=wx.Button(panel, label="Join Game", pos=(600,100),size=(200,100))
        self.receiveButton.Bind(wx.EVT_BUTTON, self.receive)
        
        self.playerList = PlayerList(parent=None, id=-1)

    def startGame(self, event):
        print "start"
        p1.main_func("1")
        self.playerList = PlayerList(parent=None, id=-1)
        self.playerList.Show()
        self.Hide()
        
    def receive(self, event):
        print "receive"
        p1.main_func("2")
        
        time.sleep(14)
        self.playerList = PlayerList(parent=None, id=-1)
        self.playerList.Show()
        self.Hide()
#        self.playerList.Refresh()

class PlayerList(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Ready Players', size=(800, 800))
        panel = wx.Panel(self)
        
        gameName = wx.StaticText(panel, -1, p1.getName()+"'s Game", (400, 50), (400, 150), wx.ALIGN_CENTER)
        readyList = wx.StaticText(panel, -1, "Ready Players", (110, 80), (150, 150))
        
        peerlist = []
        for msg in p1.peerlist:
            peerlist.append(msg.name)
        
        self.userlistbox = wx.ListBox(panel, -1, (100,100), (400,500), peerlist)
        
        button=wx.Button(panel, label="Start Game", pos=(600,500),size=(100,100))
        self.Bind(wx.EVT_BUTTON, self.startGame, button)
    
    def startGame(self, event):
        drawingBorad = DrawingBorad(parent=None, id=-1)
        drawingBorad.Show()
        
class DrawingBorad(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Zatacka', size=(800, 800))
        panel = wx.Panel(self)

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
        txt = txt + ", "
        custom1 = wx.StaticText(panel, -1, txt, (280, 80), (500, -1), wx.ALIGN_CENTER)
        custom1.SetFont(font)
        
    def closebutton(self, event):
        self.Close(True)
  
if __name__=='__main__':
    app = wx.PySimpleApp()
    p1 = Player()
    t = Table('table1', p1)
    t.addPlayer(p1)
    userlist = t.getPlayerNames()
    print userlist
    startFrame = StartPage(userlist, parent=None, id=-1)
    startFrame.Show()
    newPlayerFrame = newPlayer(parent=None, id=1)
    newPlayerFrame.Show()
    
    app.MainLoop()
    