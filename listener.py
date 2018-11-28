import socket
import sqlite3
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8888))


def handle(client: socket.socket):
    f = client.makefile('r')
    dbConn = sqlite3.connect('bees.db')
    cursor = dbConn.cursor()
    for line in f:
        size, speed = [int(x) for x in line.split(',')]
        cursor.execute('INSERT INTO bees(size, speed) VALUES ({:d}, {:d})'.format(size, speed))


s.listen(10)
while 1:
    conn, addr = s.accept()
    Thread(target=handle, args=(conn,)).start()
