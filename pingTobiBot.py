import threading
import telepot
import json
import subprocess
import re
import sys

listaThreads=[]
tobiBot = telepot.Bot('365404534:AAH4ZGos10NqOcYid4SgTp3iotqNgzTNOcg')
fileUtenti = open('jason.json').read()
users = json.loads(fileUtenti)


class pingThread(threading.Thread):
	def __init__(self, cid, addr):
		threading.Thread.__init__(self)
		self.chatID = cid
		self.ip = addr
		self.vivo = True
	def run(self):
		while (self.vivo):
			ping = 'ping -n 2 ' + self.ip
			(out) = subprocess.Popen(ping, stdout=subprocess.PIPE, shell=True).communicate()
			if re.search('Ricevuti = 0', str(out)):
				tobiBot.sendMessage(self.chatID, str(self.ip) + ' offline')
			else:
				tobiBot.sendMessage(self.chatID, str(self.ip) + ' online')

#estrai il dizionario
#per ogni ip dell'user crei un thread
for key in users:
	a = users[key]
	for kkey in a:
		for ips in a[kkey]:
			print ips
			t1 = pingThread(str(key), str(ips))
			listaThreads.append(t1)
			t1.start()

ki = ''
#while ki == '':
for t in listaThreads:
	ki = sys.stdin.read(1)
	t.vivo = False
	t.join()
