import threading
import telepot
import json
import subprocess
import re
import sys
import datetime
import urllib2

class pingThread(threading.Thread):
	def __init__(self, cid, addr):
		threading.Thread.__init__(self)
		self.chatID = cid
		self.ip = addr
		self.vivo = True
		self.change = 0
	def run(self):
		while (self.vivo):
			ping = 'ping -n 2 ' + self.ip
			(out) = subprocess.Popen(ping, stdout=subprocess.PIPE, shell=True).communicate()
			if re.search('Ricevuti = 0', str(out)):
				if (self.change == 0 or self.change == 2):
					print self.chatID + ', ' + self.ip + ', dead\n'
					tobiBot.sendMessage(self.chatID, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ', ' + self.chatID + ', ' + self.ip + ', dead\n')
					self.change = 1
				lockLog.acquire()
				logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ', ' + self.chatID + ', ' + self.ip + ', dead\n')
				lockLog.release()
			else:
				if (self.change == 0 or self.change == 1):
					print self.chatID + ', ' + self.ip + ', alive\n'
					tobiBot.sendMessage(self.chatID, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ', ' + self.chatID + ', ' + self.ip + ', alive\n')
					self.change = 2
				lockLog.acquire()
				logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ', ' + self.chatID + ', ' + self.ip + ', alive\n')
				lockLog.release()
def getUpdates(tkn):
	source = urllib2.urlopen('https://api.telegram.org/bot'+ tkn +'/getUpdates').read()
	listaIDS = re.findall('\"id\":([0-9]+),\"is_bot\"', source)
	new = []  #listaids contiene tanti id uguali, filtro in newids solo quelli diversi
	for i in listaIDS:
	  if i not in new:
	    new.append(i)
	return new

def caricaJson(filename):
	with open('hosts.json', mode='r') as dizionario:
	    utenti = json.load(dizionario)
	return utenti

token = '365404534:AAH4ZGos10NqOcYid4SgTp3iotqNgzTNOcg'
newIDS = getUpdates(token)
listaThreads=[]
tobiBot = telepot.Bot(token)
filename = 'hosts.json'
users = caricaJson(filename)
ids = users.keys() #ids contiene tutti i chatid del file json. voglio aggiungere al json anche i nuovi id trovati con l'update
#con questo for controllo che negli users del json non ci siano gia presenti dei chatid trovati nel getUpdate
for i in newIDS:
	if i not in ids:
		ids.append(i)
a = {"ip": ["192.168.100.1", "8.8.8.8", "192.168.254.1"]}
for i in ids:
	print i
	entry = {i:a} #creo un dizionario con chatid:lista ip (sempre uguale)
	users.update(entry) #appendo il dizionario appena creat a quelli che avevo gia nel dizionario json
with open('hosts.json', mode='w') as dizionario:
    json.dump(users, dizionario) #riscrivo tutto sul file json aggiornato

logFile = open('pingTobi.log', 'w')
logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ', startLog\n')
lockLog = threading.Lock()

for key in users:
	a = users[key]
	for kkey in a:
		for ips in a[kkey]:
			t1 = pingThread(str(key), str(ips))
			listaThreads.append(t1)
			t1.start()
ki = sys.stdin.read(1)
logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ', endLog\n')
for t in listaThreads:
	t.vivo = False
	t.join()

logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ', endLog\n')
logFile.close()
