import socket
import sys

class Client:
	def __init__(self, server_name, port, player_name):
		self._s = socket.socket()
		self.last_move = None
		self.over = False
		self.board = [[0 for y in xrange(9)] for x in xrange(9)]
		err = self._s.connect_ex((server_name, port))
		if err:
			print "Error connecting to server"
			exit()

		self.send("START %s" % player_name)
		print "Connected. Waiting for game to start..."
		res = self.recv()
		print res
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
			print "Opponents played %d,%d" % self.last_move
		return

	def parse_move(self, msg):
		(x, y) = (int(msg.split(" ")[1]), int(msg.split(" ")[2]))
		self.board[x][y] = (self.id + 1) % 2
		return (x, y)

	def play_move(self):
		move = play(self.last_move, self.board)
		self.board[move[0]][move[1]] = self.id
		self.send("%d %d %d" % (self.id, move[0], move[1]))

	def send(self, str):
		self._s.send("%s\n" % str)
		return

	def recv(self):
		return self._s.recv(256)






"""
Modify this method for your AI

last_move: (int, int) tuple. Contains the last move that was played by the opponent, if you
are the first to play, last_move will be None

board: a 9x9 int 2d array. 0 if the cell is empty, 1 if white, 2 if black. The current state
of the board.


returns: (int, int) tuple that is a valid move. If it's not valid then
you will lose the game and fail the course.

"""
def play(last_move, board):
	(x, y) = (0, 0)

	move = (x, y)
	return move





def main():
	Client("localhost", 8123, "pybot")

if __name__ == "__main__":main()