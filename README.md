# socket-chat-terminal
A terminal (CLI) multi-client chat application using sockets and threading from Python

This program is motivated from Georgia Tech's CS3251 - Computer Networking and includes extended functionalities.

## Libraries
- threading
- socket
- argparse
- sys
## Concepts
- multiple TCP connection
- multiple clients and a single server
- text parsing
## Functionalities 
- the client takes the server's IP address and listening port, the username, and the password
- the server takes its listening port and the password.
- client can be connected only if the password matches the server's password
- server can display multiple clients sending messages simultaneously
