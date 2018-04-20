# HELPER CLASS FOR DMD 

import socket

class LightCrafter():
	
	def __init__(self):
		
		# init connection with DMD over ethernet
		# default IP and port for DLP Lightcrafter
		self.TCP_IP = '192.168.1.100'
		self.TCP_PORT = 0x5555
		
		# open socket
		# specify SOCK_RAW param, as data isn't being sent continuously 
		self.dmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.dmdSocket.connect((TCP_IP, TCP_PORT))
		
		# set board mode to static image/test pattern
		self.dmdSocket.send(b'\x02\x01\x01\x00\x01\x00\x00\x05')
		
	def getVersion(self):
		
		self.dmdSocket.send(b'\x04\x01\x00\x00\x01\x00\x00\x06')
		return self.dmdSocket.recv(256)
		
	def setImage(self, bitmap):
		
		# convert bmp image to byte array
		bmp = bytearray(bitmap)
		
		# init start of command
				
		baseCmd = b'\x02\x01\x05'
		flag = b'\x01'
		payloadLen = b'\xFF\xFF'
		
		
		# split up image as max command payload is 64K bytes	
		step = 65535
		for i in range(0,len(bmp), step):
			
			payload = bmp[i:i+step]
			
			if i > 0:
				flag = b'\x02'
				
			if len(payload) < step:
				flag = b'\x03'
				payloadLen = bytearray(len(payload))
				payloadLen [0], payloadLen[1] = payloadLen [1], payloadLen[0]
				
				
			setImageCmd = baseCmd.append(flag.append(payLoadLen.append(payload)))
			
			checksum = bytearray(sum(setImageCmd))
			
			setImageCmd.append(checksum)
			
			self.dmdSocket.send(setImageCmd)
			
			
				

		
	def __del__(self):
		
		self.dmdSocket.close()
