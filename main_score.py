import sys

from bowling.game import BowlingGame

if __name__ == '__main__':
    throwing = []
    if len(sys.argv) > 1:
        throwing = [int(arg) for arg in sys.argv[1:]]
    print(BowlingGame.computeScore(throwing))
