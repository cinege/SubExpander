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

text_file = open("C:\\!sajat\\film\\Northern Exposure Season 3\\Northern.Exposure.S03E19.DVDRip.XviD-SFM.srt", "r")
out_file = open("C:\\!sajat\\film\\Northern Exposure Season 3\\19v8.srt", "w")
sys.stdout = out_file

lines = text_file.read().split('\n')
filmstartfrom = timeconvert("00:00:04,750")
filmstartuntil = timeconvert("00:00:07,100")
filmend = timeconvert("00:41:52,000")
substartfrom = timeconvert(lines[1][:12])
substartuntil = timeconvert(lines[1][-12:])
subendfrom = timeconvert(lines[len(lines)-4][:12])
subenduntil = timeconvert(lines[len(lines)-4][-12:])
filmduration = filmend - filmstartfrom
subduration1 = subendfrom - substartfrom
subduration2 = subenduntil - substartuntil
subduration = (subduration1 + subduration2) / 2 
ratio = filmduration / subduration1

for line in lines :
	if (len(line) == 29) :
		if (line[2] == ":" and line[5] == ":") :
			suboldfrom = timeconvert(line[:12])
			subolduntil = timeconvert(line[-12:])
			subnewfrom = amendtime(suboldfrom, filmstartfrom, ratio)
			subnewuntil = amendtime(subolduntil, filmstartuntil, ratio)
			newline =  convertback(subnewfrom) + " " + "-->" + " " + convertback(subnewuntil)
			print (newline)
		else :
			print (line)
	else :
		print (line)
text_file.close()
out_file.close()