from typing import List, Dict, Optional, Union

from .const import NUMBER_OF_PINS, PLAYER_NAME, PLAYER_SCORE
from .frame import BowlingFrame, PinsOverflowError

__author__ = 'Anthony Rouneau'


class BowlingGame:
    """
    Class defining a Bowling game, containing players and keeping scores.
    """

    def __init__(self, players: List[PLAYER_NAME]):
        """
        Creates a new Bowling game.
        
        Args:
            players: A list containing the name of all the players taking part to this game.  
        """
        self.players = players  # type: List[PLAYER_NAME]
        self.scores = {player: 0 for player in self.players}  # type: Dict[PLAYER_NAME, PLAYER_SCORE]
        self.frames = {player: [] for player in self.players}  # type: Dict[PLAYER_NAME, List[BowlingFrame]]

    def play(self):
        """
        Launch the bowling game.
        """
        while len(self.frames[self.players[-1]]) != 10:
            for player in self.players:
                new_frame = BowlingFrame(player, ending=len(self.frames[player]) == 9)
                self.frames[player].append(new_frame)
                while not new_frame.isFinished:
                    try:
                        nb_pins = int(input("Please indicate the number of rows knocked down by %s: "
                                            % player))
                        new_frame.registerThrowing(nb_pins)
                        self._informPreviousFrames(self.frames[player])
                        print(self)
                    except ValueError:
                        print("Incorrect value")
                        continue
                    except PinsOverflowError as error:
                        print("\n/!\\ %s /!\\ \n" % str(error))
                        continue

    @staticmethod
    def computeScoreOnFrames(frames: List[BowlingFrame]) -> int:
        """
        Computes the score of finished bowling frames
        
        Args:
            frames: The frames from which the score will be computed

        Returns: The final score obtained by the given frames

        """
        if len(frames) == 0:
            return 0
        for frame in frames:
            if not frame.isFinished:
                raise ValueError("Cannot compute the score of unfinished frames")
        for i in range(2, len(frames) + 1):
            BowlingGame._informPreviousFrames(frames[:i])
        return frames[-1].getScore()

    @staticmethod
    def computeScore(throwing_list: List[NUMBER_OF_PINS]) -> Union[int, None]:
        """
        Computes the score of a Bowling game, given the number of pins that the player knocked down at each throwing.
        Limits itself at 10 frames. The given list of throwing must contain enough throwing to complete 
        a certain number (in [0, 10]) of frames. If the throwing leave a frame uncompleted, the method
        will raise an error.
        
        Args:
            throwing_list: 
                The list containing the number of pins knocked down at each throwing if it is defined.
                If the score can not be defined yet, return None
             

        Returns: The score obtained for the given list of throwing
        
        Raises:
            ValueError: If there are not enough throwing to complete one or multiple frames.
        """
        frames = []  # type: List[BowlingFrame]
        index = 0
        while len(frames) != 10 and index != len(throwing_list):
            new_frame = BowlingFrame("player", ending=len(frames) == 9)
            while not new_frame.isFinished:
                try:
                    new_frame.registerThrowing(throwing_list[index])
                    index += 1
                except IndexError:
                    raise ValueError("Not enough pins have been knocked down to finish the frame %d"
                                     % (len(frames) + 1))
            frames.append(new_frame)
        return BowlingGame.computeScoreOnFrames(frames)

    @staticmethod
    def _informPreviousFrames(frames: List[BowlingFrame]):
        """
        Inform the two last frames from the new frame.

        Args:
            frames: The list of frames to inform.
        """
        if len(frames) >= 3:
            frames[-3].computeScore(frames[-2], frames[-1])
        if len(frames) >= 2:
            frames[-2].computeScore(frames[-1])

    def __str__(self):
        string = "\n"
        for player, frames in self.frames.items():
            string += player + '\n'
            for frame in frames:
                string += frame.__str__() + ' '
            string += '\n'
            for frame in frames:
                string += frame.__str__(True) + ' '
            string += '\n\n'
        return string