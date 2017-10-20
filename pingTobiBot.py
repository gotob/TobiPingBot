import threading
import telepot
import json

tobiBot = telepot.Bot('365404534:AAH4ZGos10NqOcYid4SgTp3iotqNgzTNOcg')
fileUtenti = file.open('jason.json').read()
users = json.loads(fileUtenti)


class pingThread(threading.Thread())
