import socket
import threading
import sys 
import argparse


#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents

def client_thread(connectionSocket, clients):
	while True:
		packet = connectionSocket.recv(4096).decode().split(' ')
		username, socketpw = packet[1], packet[0]

		if len(socketpw) > 5 or (not socketpw.isalnum()) or passcode != socketpw:
			connectionSocket.send('Incorrect passcode'.encode())
		else:
			# no need to worry about string being 'good' as this loop breaks once satisfied
			connectionSocket.send('good'.encode())
			print(f'{username} joined the chatroom')
			sys.stdout.flush()
			
			for client in clients:
				if connectionSocket.getpeername()[1] != client.getpeername()[1]:
					client.send(f'{username} joined the chatroom'.encode())
			break


	while True: 
		try:
			sentence = connectionSocket.recv(4096).decode()
			if not sentence:
				print('Client connection closed')
				sys.stdout.flush()
				break
			if sentence == ':Exit':
				# close the socket that entered ':Exit'
				connectionSocket.close()
				# remove socket from list so that later chat inputs does not create error
				clients.remove(connectionSocket)
				for client in clients:
					client.send(f'{username} left the chatroom'.encode())
			else:
				print(f'{username}: {sentence}')
				sys.stdout.flush()

				for client in clients:
					# send message to other clients except itself
					if connectionSocket.getpeername()[1] != client.getpeername()[1]:
						client.send(f'{username}: {sentence}'.encode())
		except ConnectionResetError as e:
			print('Client connection closed')
			break 
		except OSError as e:
			print(f'{username} left the chatroom')
			sys.stdout.flush()
			break
	


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-start', nargs='*')
	parser.add_argument('-port', type=int, required=True)
	parser.add_argument('-passcode', type=str, required=True)

	args = parser.parse_args()
	portNum, passcode = args.port, args.passcode

	serverPort = args.port
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# establish welcoming door
	serverSocket.bind(('', serverPort))
	# specifies the maximum number of queued connections
	serverSocket.listen(10)

	print(f'Server started on port {portNum}. Accepting connections')
	sys.stdout.flush()

	# list that contains all of the clients (socket objects)
	clients = []
	while True:
		connectionSocket, addr = serverSocket.accept()
		clients.append(connectionSocket)

		# use a thread to handle multiple clients
		t = threading.Thread(target=client_thread, args=(connectionSocket, clients, ))
		t.start()

	