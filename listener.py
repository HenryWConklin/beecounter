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
        print(line)
        size, speed = [float(x) for x in line.split(',')]
        sql = 'INSERT INTO bees(size, speed) VALUES (?, ?);'
        cursor.execute(sql, (size, speed))
    dbConn.commit()
    cursor.close()
    dbConn.close()


s.listen(10)
while 1:
    conn, addr = s.accept()
    print("Connection from: " + str(addr))
    Thread(target=handle, args=(conn,)).start()
