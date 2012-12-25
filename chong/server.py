import chong
from boardserver import server

board = chong.Board()
api = server.Server(board)
api.run()
