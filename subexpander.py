
import wx
import sys

def compl2(number) :
	digits = str(number)
	if (len(digits) == 1) :
		digits = "0" + digits
	return digits
	
def compl3(number) :
	digits = str(number)
	if (len(digits) == 1) :
		digits = "0" + digits
	if (len(digits) == 2) :
		digits = "0" + digits
	return digits

def timeconvert(time) :
	hour = int(time[:2])
	min = int(time[:5][-2:])
	sec = int(time[:8][-2:])
	milsec = int(time[-3:])
	duration = (3600 * hour + 60 * min + sec) * 1000 + milsec
	return duration

def convertback(durinmilsec) :
	hour = int(divmod(durinmilsec, 3600000)[0])
	remains = divmod(durinmilsec, 3600000)[1]
	min = int(divmod(remains, 60000)[0])
	remains = divmod(remains, 60000)[1]
	sec = int(divmod(remains, 1000)[0])
	remains = divmod(remains, 1000)[1]
	milsec = int(remains)
	time = compl2(hour) + ":" + compl2(min) + ":" + compl2(sec) + "," + compl3(milsec)
	return time

def amendtime(suboldtime, filmstart, ratio) :
		subnewtime = filmstart + (suboldtime - filmstart) * ratio
		return subnewtime	

class Frame(wx.Frame):
	def __init__(self, title):
		#GUI
		wx.Frame.__init__(self, None, title=title, size=(600,600))
		self.filepathtitle = wx.StaticText(self,1,label="Forras File:",style = wx.ALIGN_LEFT,pos=(10,20))
		self.filepathfield = wx.TextCtrl(self,id=2,size=(450,30),pos=(10,60))
		self.firstsubtitle = wx.StaticText(self,4,label="Elso felirat - kezdeti idopont: (hh:mm:ss,milsec)",style = wx.ALIGN_LEFT,pos=(10,100))
		self.firstsubfield = wx.TextCtrl(self,id=5,size=(100,30),pos=(10,130))
		self.lastsubtitle = wx.StaticText(self,6,label="Utolso felirat - kezdeti idopont: (hh:mm:ss,milsec)",style = wx.ALIGN_LEFT,pos=(10,200))
		self.lastsubfield = wx.TextCtrl(self,id=7,size=(100,30),pos=(10,230))
		
		self.loadbutton = wx.Button(self,id=3,label="Megnyit",size=(100,30),pos=(480,60))
		self.genbutton = wx.Button(self,id=8,label="Uj feliratfile letrehozasa",size=(400,30),pos=(10,280))
		self.closebutton = wx.Button(self,id=90,label="Bezar",size=(100,50),pos=(480,500))

		self.loadbutton.Bind(wx.EVT_BUTTON, self.LoadSUB, id=3)
		self.genbutton.Bind(wx.EVT_BUTTON, self.ExpandSUB, id=8)
		self.closebutton.Bind(wx.EVT_BUTTON, self.OnClose, id=90)
		

	def LoadSUB(self, event):
		self.srtfile = wx.FileDialog(self, "Open SRT file", wildcard="SRT files (*.srt)|*.srt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		self.srtfile.ShowModal()
		self.filepath = (self.srtfile.GetPath())
		input_file = open(self.filepath, "r")
		arrow = "-->"
		self.lines = input_file.read().split('\n')
		#First Subtitle
		i = 0
		while arrow not in self.lines[i]:
			i = i + 1
		firstsubstart = self.lines[i][:12]
		firstsubend = self.lines[i][-12:]
		#Last Subtitle
		i = len(self.lines)-1
		while arrow not in self.lines[i]:
			i = i - 1
		lastsubstart = self.lines[i][:12]
		# fill in the 3 fields	
		self.filepathfield.SetValue(self.filepath)
		self.firstsubfield.SetValue(firstsubstart)
		self.lastsubfield.SetValue(lastsubstart)
		# 
		self.a1 = timeconvert(firstsubstart)
		self.b1 = timeconvert(firstsubend)
		self.an = timeconvert(lastsubstart)
		input_file.close()
	
	def ExpandSUB(self, event):
			
		# These values were manually adjusted
		a1 = self.a1
		b1 = self.b1
		an = self.an
		# bn not available / not relevant 
		a1v = timeconvert(self.firstsubfield.GetValue())
		anv = timeconvert(self.lastsubfield.GetValue())
		# b1-a1 = b1v-a1v -----> b1v = a1v + b1 - a1
		b1v = a1v + b1 - a1 
		# The multiplicator which expands or shrinks the subtitle time entries
		ratio = (anv-a1v)/(an-a1)
		
		out_file = open(self.filepath + "_v2.srt", "w")
		sys.stdout = out_file
				
		for line in self.lines :
			if (len(line) == 29 and line[2] == ":" and line[5] == ":") :
				ak = timeconvert(line[:12])
				bk = timeconvert(line[-12:])
				akv = a1v + (ak - a1) * ratio
				bkv = b1v + (bk - b1) * ratio
				newline =  convertback(akv) + " " + "-->" + " " + convertback(bkv)
				print (newline)
			else:
				print (line)
		out_file.close()
	
	def OnClose(self, event):
		self.Close()
		
app = wx.App()
top = Frame("Felirat megnyujtasa...")
top.Show()
app.MainLoop()