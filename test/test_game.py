from unittest import TestCase

from bowling.frame import BowlingFrame
from bowling.game import BowlingGame


class TestBowlingGame(TestCase):
    def test_compute_max_score_on_frames(self):
        """
        Tests if the maximum score is computed correctly
        """
        frames = []
        for _ in range(9):
            frame = BowlingFrame("test")
            frame.registerThrowing(10)
            frames.append(frame)
        frame = BowlingFrame("test", ending=True)
        # Three strikes are allowed in the ending frame
        frame.registerThrowing(10)
        frame.registerThrowing(10)
        frame.registerThrowing(10)
        frames.append(frame)
        self.assertEqual(BowlingGame.computeScoreOnFrames(frames), 300)

    def test_compute_score_on_frames(self):
        """
        Tests if the score is computed correctly on a typical game
        """
        frames = []

        frame = BowlingFrame("test")
        frame.registerThrowing(2)
        frame.registerThrowing(3)
        frames.append(frame)
        frame = BowlingFrame("test")
        frame.registerThrowing(6)
        frame.registerThrowing(4)
        frames.append(frame)  # Spare
        frame = BowlingFrame("test")
        frame.registerThrowing(8)
        frame.registerThrowing(1)
        frames.append(frame)
        frame = BowlingFrame("test")
        frame.registerThrowing(10)
        frames.append(frame)  # Strike
        frame = BowlingFrame("test")
        frame.registerThrowing(3)
        frame.registerThrowing(0)
        frames.append(frame)
        frame = BowlingFrame("test")
        frame.registerThrowing(10)
        frames.append(frame)  # Strike
        frame = BowlingFrame("test")
        frame.registerThrowing(10)
        frames.append(frame)  # Strike
        frame = BowlingFrame("test")
        frame.registerThrowing(10)
        frames.append(frame)  # Strike
        frame = BowlingFrame("test")
        frame.registerThrowing(10)
        frames.append(frame)  # Strike
        frame = BowlingFrame("test", ending=True)
        frame.registerThrowing(1)
        frame.registerThrowing(9)
        frame.registerThrowing(5)
        frames.append(frame)
        self.assertEqual(BowlingGame.computeScoreOnFrames(frames), 164)

    def test_compute_incomplete_score_on_frames(self):
        """
        Tests if the score is computed correctly on an incomplete game
        """
        frames = []

        frame = BowlingFrame("test")
        frame.registerThrowing(2)
        frame.registerThrowing(3)
        frames.append(frame)
        frame = BowlingFrame("test")
        frame.registerThrowing(6)
        frame.registerThrowing(4)
        frames.append(frame)  # Spare
        frame = BowlingFrame("test")
        frame.registerThrowing(8)
        frame.registerThrowing(1)
        frames.append(frame)
        frame = BowlingFrame("test")
        frame.registerThrowing(10)
        frames.append(frame)  # Strike
        frame = BowlingFrame("test")
        frame.registerThrowing(3)
        frame.registerThrowing(0)
        frames.append(frame)
        self.assertEqual(BowlingGame.computeScoreOnFrames(frames), 48)

    def test_compute_undefined_score_on_frames(self):
        """
        Tests if the score is undefined on an incomplete game ending on a strike
        """
        frames = []

        frame = BowlingFrame("test")
        frame.registerThrowing(2)
        frame.registerThrowing(3)
        frames.append(frame)
        frame = BowlingFrame("test")
        frame.registerThrowing(6)
        frame.registerThrowing(4)
        frames.append(frame)  # Spare
        frame = BowlingFrame("test")
        frame.registerThrowing(8)
        frame.registerThrowing(1)
        frames.append(frame)
        frame = BowlingFrame("test")
        frame.registerThrowing(10)
        frames.append(frame)  # Strike
        self.assertEqual(BowlingGame.computeScoreOnFrames(frames), None)

    def test_compute_max_score(self):
        """
        Tests if the maximum score is computed correctly without frames
        """
        pins = [10 for _ in range(12)]
        self.assertEqual(BowlingGame.computeScore(pins), 300)

    def test_compute_score(self):
        """
        Tests if the score is computed correctly without frames on a typical game
        """
        pins = [2, 3, 6, 4, 8, 1, 10, 3, 0, 10, 10, 10, 10, 1, 9, 5]
        self.assertEqual(BowlingGame.computeScore(pins), 164)

    def test_error_incomplete_frame(self):
        """
        Tests if the good error is raised when a frame is not complete
        """
        pins = [2, 3, 6, 4, 8, 1, 10, 3, 0, 10, 10, 10, 10, 1, 9]
        self.assertRaises(ValueError, BowlingGame.computeScore, pins)

    def test_error_incomplete_frame2(self):
        """
        Tests if the good error is raised when a frame is not complete
        """
        frames = [BowlingFrame("test")]
        self.assertRaises(ValueError, BowlingGame.computeScoreOnFrames, frames)

    def test_score_empty_game(self):
        """
        Tests if the score of an empty game is 0
        """
        self.assertEqual(BowlingGame.computeScoreOnFrames([]), 0)
        self.assertEqual(BowlingGame.computeScore([]), 0)

    def test_str(self):
        """
        Tests if the string representation of the game is correct
        """
        frame1 = BowlingFrame("test")
        frame2 = BowlingFrame("test")
        game = BowlingGame(['test'])
        game.frames = {"test": [frame1, frame2]}
        representation = 'test\n' + frame1.__str__() + ' ' + frame2.__str__() + ' \n' + \
                         frame1.__str__(True) + ' ' + frame2.__str__(True) + ' \n'
        self.assertEqual(str(game).strip(), representation.strip())

    def test_play(self):
        """
        Tests if the play build up correctly
        """
        game = BowlingGame(['test'])
        game.play([2, 3, 6, 4, 8, 1, 10, 3, 0, 10, 10, 10, 10, 1, 9, 5], verbose=False)
        self.assertEqual(len(game.frames['test']), 10)
        self.assertEqual(BowlingGame.computeScoreOnFrames(game.frames['test']), 164)

