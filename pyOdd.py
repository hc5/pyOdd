import socket
import sys

INVALID = -1
EMPTY = 0
WHITE = 1
BLACK = 2

class Client:
	def __init__(self, server_name, port, player_name):
		self.last_move = None
		self.over = False
		self.board = [[INVALID if  x - y <-4 or x - y > 4 else EMPTY for y in xrange(9)] for x in xrange(9)]
		self._s = socket.socket()
		print "Connecting to server"
		err = self._s.connect_ex((server_name, port))
		if err:
			print "Error connecting to server"
			exit()

		self.send("START %s" % player_name)
		print "Connected. Waiting for game to start..."
		res = self.recv()
		start()
		self.id = int(res[12])
		while not self.over:
			res = self.recv()
			if res and len(res.strip()):
				self.procMsg(res)
		self._s.close()

	def procMsg(self, msg):
		msg = msg.strip()
		print "PROCMSG: \"%s\"" % msg
		if msg.startswith("GAMEOVER"):
			print msg
			self.over = True
		elif msg.startswith("PLAY"):
			self.play_move()
		else:
			self.last_move = self.parse_move(msg)
			print "Opponents played %d,%d,%d" % self.last_move
		return

	def parse_move(self, msg):
		(c, x, y) = (0 if msg.split(" ")[1] == "WHITE" else 1, int(msg.split(" ")[2])+4, int(msg.split(" ")[3])+4)
		self.board[x][y] = c
		return (c,x, y)

	def play_move(self):
		move = play(self.last_move, self.board)
		self.board[move[1]][move[2]] = move[0]	
		colours = ["WHITE","BLACK"]
		self.send("%d %s %d %d" % (self.id,colours[move[0]-1], move[1]-4, move[2]-4))

	def send(self, s):
		self._s.send("%s\n" % s)
		return

	def recv(self):
		return self._s.recv(256)






"""
Modify this method for your AI

In the playing board the center is (0,0), which makes the bottom left (-4,-4) and the 
top right (4,4), which is difficult to work with. The board of this python client is 
a 9x9 2d array, and it starts at (0,0) at the bottom left corner, and (8,8) at the top
 right corner which makes it a lot simpler to work with.

When the `last_move` param is given in the shifted coordinate system from (0,0) to 
(8,8), and the `move` tuple you return should also be in the shifted coordinate system.


last_move: (int colour, int x, int y) tuple. Contains the last move that was played by the opponent, if you
are the first to play, last_move will be None

board: a 9x9 int 2d array. 0 if the cell is empty, 1 if white, 2 if black, and -1 if the cell
 is invalid. The current state of the board.


returns: (int colour, int x, int y) tuple that is a valid move. If it's not valid then
you will lose the game and fail the course. 

"""

def play(last_move, board):
	(c, x, y) = (WHITE, 0, 0)

	move = (c, x, y)
	return move


"""
This is called when the game starts, do any initializations here
"""
def start():
	print "Game started"

def print_board(board):
	lines = []
	for i in xrange(4,-5,-1):
		line = ""
		line+= " "*(4-i+len(xrange(0,i)))
		for j in xrange(-4,5):
			symbols = {-1:" ", 0:"+ ", 1:"O ", 2:"@ "}
			line += symbols[board[i+4][j+4]]
		lines.append(line)
	print "\n".join(lines)




def main():
	if len(sys.argv) > 1:
		Client(sys.argv[1], int(sys.argv[2]), "pybot")
	Client("localhost", 8123, "pybot")



if __name__ == "__main__":main()