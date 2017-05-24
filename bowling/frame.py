from typing import Tuple, Optional, Union

from .const import PLAYER_NAME, NUMBER_OF_PINS

__author__ = 'Anthony Rouneau'


class BowlingFrame:
    """
    Class defining a bowling frame for one player. 
    There are 10 frames per player in a bowling game.
    """

    def __init__(self, player: PLAYER_NAME, ending: bool = False):
        """
        Creates a new Bowling frame for the given player.
        
        Args:
            player: The name of the player taking part in this frame.
            ending: Boolean indicating whether this frame is the final frame in the game.
        """
        self.player = player
        self.isFinished = False
        self.ending = ending
        self._score = None
        self._throwing = ()  # type: Tuple[NUMBER_OF_PINS, ...]
        self._previousScore = 0

    def getScore(self) -> Union[int, None]:
        """
        Returns: None if the score cannot be computed yet. Else, returns the accumulated score.
        """
        if self._score is None:
            return None
        return self._previousScore + self._score

    def setPreviousScore(self, previous_score: int):
        """
        Update the score already accumulated before this frame.
        
        Args:
            previous_score: The previous score to update.
        """
        self._previousScore = previous_score

    def isStrike(self) -> bool:
        """
        Returns: True if the player has performed a strike during this frame.
        """
        return len(self._throwing) >= 1 and self.getNbOfKnockedDownPins(1) == 10

    def isSpare(self) -> bool:
        """
        Returns: True if the player has performed a spare during this frame.
        """
        return not self.isStrike() and self.getNbOfKnockedDownPins(2) == 10

    def isHole(self) -> bool:
        """
        Returns: True if the player has neither performed a strike or a spare.
        """
        return self.isFinished and self.getNbOfKnockedDownPins() < 10

    def getThrowing(self) -> Tuple[NUMBER_OF_PINS, ...]:
        """
        Returns: The results of this frame.
        """
        return self._throwing

    def getNbOfKnockedDownPins(self, max_size: int = -1) -> NUMBER_OF_PINS:
        """
        Args:
            max_size: The maximum number of throwing to consider in this number of knocked down pins (-1 means no limit)
            
        Returns: The number of pins knocked down until now.
        """
        if max_size == -1:
            max_size = len(self._throwing)
        return sum(self._throwing[:max_size])

    def registerThrowing(self, nb_pins: NUMBER_OF_PINS):
        """
        Register the result of the current throwing.
        
        Args:
            nb_pins: The number of pins that fell during this throwing.
        """
        if not self.isFinished:
            if nb_pins < 0:
                raise ValueError("Cannot knock down a negative number of pins")
            self._throwing += (nb_pins,)
            throwing = self._throwing

            total_nb_pins = self.getNbOfKnockedDownPins()
            if total_nb_pins > 10 and not self.ending:
                self._throwing = throwing[:-1]  # Cancels the last throwing.
                raise PinsOverflowError("There are only 10 pins and %s has, supposedly, knocked down %d pins"
                                        % (self.player, total_nb_pins))

            if len(throwing) == 3 or (len(throwing) == 2 and (not self.ending or total_nb_pins < 10)) \
                    or (not self.ending and self.isStrike()):
                self.isFinished = True
                self.computeScore()

    def computeScore(self, next_frame: Optional['BowlingFrame'] = None,
                     next_next_frame: Optional['BowlingFrame'] = None):
        """
        Computes the score of this frame.
        
        Args:
            next_frame: The direct next frames if needed to compute the score.
            next_next_frame: The second next frame, useful if the next frame is a strike.
        """
        if self.isWaitingForNextRound():
            # The score has not already been set
            total_nb_pins = self.getNbOfKnockedDownPins()
            if next_frame is None:
                if self.isHole() or self.ending:
                    self._score = total_nb_pins

            else:
                if self.isSpare():
                    self._score = total_nb_pins + next_frame._throwing[0]

                elif self.isStrike() and (next_frame.isFinished or len(next_frame.getThrowing()) >= 2):
                    # A strike occurred in this frame, hence, the points must be accumulated with the next frame
                    #  and with the first throwing of the frame after that if the direct next frame has also a strike.
                    potential_score = total_nb_pins + next_frame.getNbOfKnockedDownPins(2)
                    if next_frame.isHole() or next_frame.isSpare() or next_frame.ending:
                        # The next frame is not a strike, so we can stop accumulating points
                        self._score = potential_score
                    elif next_next_frame is not None and len(next_next_frame.getThrowing()) >= 1:
                        # The next frame is a strike and the frame after that can be used
                        self._score = potential_score + next_next_frame.getNbOfKnockedDownPins(1)
        if self.getScore() is not None and next_frame is not None:
            # We can propagate the score of this frame to the next one once it is set.
            next_frame.setPreviousScore(self.getScore())

    def isWaitingForNextRound(self) -> bool:
        """
        Returns: True if the score of this frame cannot be determined yet because of a strike or a spare.
        """
        return self._score is None

    def __str__(self, score: bool = False) -> str:
        """
        Gives a string representation of this frame.
        Based on two lines, which can be obtained by two calls to this function.
        The first call with score = False, which will give the throwing of this frame.
        The second call with score  = True, which will display the score of this frame if it is defined.
        
        Args:
            score: Boolean indicating whether the score only, or the throwing only must be displayed. 

        Returns: A string that represents this frame
        """
        if score:
            score_len = 7 if not self.ending else 9
            score_str = '|' + (score_len - 2) * ' ' + '|'
            if self.getScore() is not None:
                score_str = '| ' + str(self.getScore())
                score_str += (score_len - len(score_str) - 1) * ' '
                score_str += '|'
            return score_str
        else:
            throwing_1 = self._throwing[0] if len(self._throwing) >= 1 else ' '
            throwing_2 = self._throwing[1] if len(self._throwing) >= 2 else ' '
            if self.isStrike():
                throwing_1 = ' ' if not self.ending else 'X'
                if not self.ending or self.getNbOfKnockedDownPins(2) >= 20:
                    throwing_2 = 'X'
            if self.isSpare():
                throwing_2 = '/'
            throwing = "| |%s|%s|" % (throwing_1, throwing_2)
            if self.ending:
                throwing_3 = self._throwing[2] if len(self._throwing) >= 3 else ' '
                if throwing_3 == 10:
                    throwing_3 = 'X'
                elif throwing_2 != 'X' and throwing_3 != ' ' and (throwing_2 + throwing_3) == 10:
                    throwing_3 = '/'
                throwing += '%s|' % throwing_3
            return throwing


class PinsOverflowError(Exception):
    """
    Class defining the error to throw when too much pins seems to have been knocked down.
    """
    pass
