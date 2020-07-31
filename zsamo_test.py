# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:32:17 2020

@author: Viktor
"""


import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect( ('192.168.1.121', 50007) )

############
msg = 'V1,600'
sock.sendall( msg.encode('ascii') )
data = sock.recv(1024)
print(data.decode('ascii'))

############
msg = 'V1,Status'
sock.sendall( msg.encode('ascii') )
data = sock.recv(1024)
print(data.decode('ascii'))

sock.close()




676
