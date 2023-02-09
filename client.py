import socket
import sys 
import argparse
import datetime
import threading

#TODO: Implement a client that connects to your server to chat with other clients here

### We have to use TCP
### Textbook 2.7

# new socket that is dedicated to a particular client: serverSocket
# newly created socket dedicated to client making the connection: connectionSocket

# Use sys.stdout.flush() after print statemtents


# function for handling message shortcuts
def is_short(message):
	if message == ':)': message = '[feeling happy]'
	elif message == ':(': message = '[feeling sad]'
	elif message == ':mytime': 
		e = datetime.datetime.now()
		message = e.strftime('%a %b %d %H:%M:%S %Y')
	elif message == ':+1hr':
		e = datetime.datetime.now() + datetime.timedelta(hours=1)
		message = e.strftime('%a %b %d %H:%M:%S %Y')
	
	return message

def receive_info(clientSocket):

	while True:
		auth_result = clientSocket.recv(4096).decode()
		if auth_result == 'good':
			print(f'Connected to {host} on port {portNum}')
			sys.stdout.flush()
		# case when there is no input from clientSocket (connection closed)
		elif not auth_result:
			return
		else:
			print(auth_result)
			sys.stdout.flush()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-join', nargs='*')
	parser.add_argument('-host', type=str, required=True)

	parser.add_argument('-port', type=int, required=True)
	parser.add_argument('-username', type=str, required=True)
	parser.add_argument('-passcode', type=str, required=True)
	args = parser.parse_args()
	
	host, portNum, username, passcode = args.host, args.port, args.username, args.passcode

	if len(username) > 8: 
		sys.exit('Maximum display name length is 8') 
	elif host != '127.0.0.1':
		sys.exit('Wrong host')


	serverName = host
	serverPort = portNum
	

	# 1st parameter: indicates using IPv4
	# 2nd paramteer: socket type is TCP
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# paramter = address of the serverside connection
	clientSocket.connect((serverName, serverPort))

	# packet contains pathcode and user name
	packet = passcode + ' ' + username
	clientSocket.send(packet.encode())


	t = threading.Thread(target=receive_info, args=(clientSocket,))
	t.start()


	while True:
		sentence = input()
		sentence = is_short(sentence)

		clientSocket.send(sentence.encode())
