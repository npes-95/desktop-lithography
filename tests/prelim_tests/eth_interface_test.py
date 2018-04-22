import socket

# default IP and port for DLP Lightcrafter
TCP_IP = '192.168.1.100'
TCP_PORT = 0x5555

# get the DM365 software version from the projector
# first six bytes are header, last byte is checksum, middle is variable length payload
versionCmd = b'\x04\x01\x00\x00\x01\x00\x00\x06'

# specify SOCK_RAW param, as data isn't being sent continuously 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# send command
s.send(versionCmd)

# get result (arbitrary buffer length here)
data = s.recv(256)

# close port
s.close()

print("version: ", ''.join([chr(elem) for elem in data[6:9]]))