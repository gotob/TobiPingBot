import threading
import telepot
import json
import subprocess
import re
#threads=[]
tobiBot = telepot.Bot('365404534:AAH4ZGos10NqOcYid4SgTp3iotqNgzTNOcg')
fileUtenti = open('jason.json').read()
users = json.loads(fileUtenti)


class pingThread(threading.Thread):
	def __init__(self, cid, addr):
		threading.Thread.__init__(self)
		self.chatID = cid
		self.ip = addr
		self.attivo=True
	def run(self):
		while (self.attivo):
			ping = 'ping -n 2 ' + self.ip
			(out) = subprocess.Popen(ping, stdout=subprocess.PIPE, shell=True).communicate()
			if re.search('Ricevuti = 0', str(out)):
				print str(out)
				tobiBot.sendMessage(self.chatID, str(self.ip) + ' offline')
			else:
				tobiBot.sendMessage(self.chatID, str(self.ip) + ' online')


#estrai il dizionario
#per ogni ip dell'user crei un thread
t1 = pingThread('164433105', '192.168.100.1')
t1.start()
