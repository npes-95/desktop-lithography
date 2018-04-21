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
		self.dmdSocket.connect((self.TCP_IP, self.TCP_PORT))
		
		# set board mode to static image/test pattern
		self.dmdSocket.send(b'\x02\x01\x01\x00\x01\x00\x00\x05')
		
	def getVersion(self):
		
		self.dmdSocket.send(b'\x04\x01\x00\x00\x01\x00\x00\x06') 
		return self.dmdSocket.recv(256)
		
	def setImage(self, bitmap):
		
		# convert bmp image to byte array
		bmp = bytearray(bitmap)
		
		# init start of command	
		baseCmd = bytearray(b'\x02\x01\x05')
		flag = bytearray(b'\x01')
		
		
		# split up image as max command payload is 64K bytes	
		step = 65535
		for i in range(0,len(bmp), step):
			
			# split payload
			payload = bmp[i:i+step]
			
			# check if flag needs to be changed (1: beginning of data, 2: middle of data, 3: end of data)
			if i > 0:
				flag = bytearray(b'\x02')
				
			if len(payload) < step:
				flag = bytearray(b'\x03')
			
			# get payload length	
			payloadLen = bytearray(len(payload).to_bytes(2, byteorder='little'))
			
			# put all the different parts of the command together	
			setImageCmd = baseCmd + flag + payloadLen + payload
			
			# calculate checksum	
			checksum = bytearray([sum(setImageCmd)%256])
			
			# add checksum to command
			setImageCmd += checksum
			
			# send command
			self.dmdSocket.send(bytes(setImageCmd))
			
			
				

		
	def __del__(self):
		
		self.dmdSocket.close()