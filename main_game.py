import sys

from bowling.game import BowlingGame

if __name__ == '__main__':
    players = ["TestPlayer"]
    if len(sys.argv) > 1:
        players = sys.argv[1:]
    game = BowlingGame(players)
    game.play()
