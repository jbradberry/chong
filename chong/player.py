import chong
from boardplayer import player


class HumanChongPlayer(player.Player):
    def get_play(self):
        while True:
            move = raw_input("Please enter your move: ")
            move = self.board.parse(move)
            if self.board.is_legal(self.states[-1], move):
                break
        return move


board = chong.Board()
player = HumanChongPlayer(board)
player.run()
