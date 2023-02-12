#!/usr/bin/env python3

import sys
import socket
import selectors
import twitchRequests
import time
import types
host = "irc.chat.twitch.tv"
port = 6667
nickname = "n0ah"
channels = twitchRequests.main()
num_conns = len(channels)


token = "oauth:nryiouttuaf2ptakfvtozo3qt92xxl"
sel = selectors.DefaultSelector()
connections = {}
dropped_conns = []

def read(conn,mask):

    try:
        data = conn.recv(1024)
        if data:
            print(data.decode('utf-8'))
        else:
            print("closin ", conn)
            sel.unregister(conn)
            dropped_conns.append(connections.pop(conn))
            conn.close()

    except ConnectionResetError:
        pass
    except ConnectionAbortedError:
        pass
    except UnicodeError:
        pass

def main():
    for channel in channels:
        time.sleep(0.2)
        try:
            sock = socket.socket()
            sock.connect((host, port))
            sock.send(f"PASS {token}\r\n".encode('utf-8'))
            sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
            sock.send(f"JOIN #{channel}\r\n".encode('utf-8'))
            sock.setblocking(False)
            connections[sock] = channel
            sel.register(sock, selectors.EVENT_READ, read)
        except ConnectionResetError:
            pass



    try:
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


    except KeyboardInterrupt:
        print(f"mahdollisia yhteyksiä:{len(channels)}")
        print(f"onnistuneita yhteyksia: {len(connections)}")
        print(f"pudotetut: {[item for item in dropped_conns]}")
        for sock in connections:
            sock.close()
        exit()

if __name__ == '__main__':
    main()



