from pyOdd import AbstractClient, BLACK, EMPTY, INVALID, WHITE

class exampleClient(AbstractClient):
	def play(self,last_move, board):
		(c, x, y) = (WHITE, 0, 0)
	
		move = (c, x, y)
		return move
	
	def start(self):
		print "Game started!"
		


exampleClient("localhost", 8123, "pybot")