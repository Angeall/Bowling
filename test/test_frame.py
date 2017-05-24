from unittest import TestCase

from bowling.frame import BowlingFrame, PinsOverflowError


class TestBowlingFrame(TestCase):
    def test_number_pins(self):
        """
        Checks if the number of knocked down pins is returned correctly
        """
        frame = BowlingFrame("test")
        self.assertEqual(frame.getNbOfKnockedDownPins(), 0)
        frame.registerThrowing(5)
        self.assertEqual(frame.getNbOfKnockedDownPins(), 5)
        frame.registerThrowing(5)
        self.assertEqual(frame.getNbOfKnockedDownPins(), 10)
        self.assertEqual(frame.getNbOfKnockedDownPins(1), 5)
        self.assertEqual(frame.getNbOfKnockedDownPins(2), 10)

    def test_number_pins_ending(self):
        """
        Checks if the number of knocked down pins is returned correctly, even for an ending frame
        """
        frame = BowlingFrame("test", ending=True)
        self.assertEqual(frame.getNbOfKnockedDownPins(), 0)
        frame.registerThrowing(5)
        self.assertEqual(frame.getNbOfKnockedDownPins(), 5)
        frame.registerThrowing(5)
        self.assertEqual(frame.getNbOfKnockedDownPins(), 10)
        frame.registerThrowing(7)
        self.assertEqual(frame.getNbOfKnockedDownPins(), 17)
        self.assertEqual(frame.getNbOfKnockedDownPins(1), 5)
        self.assertEqual(frame.getNbOfKnockedDownPins(2), 10)
        self.assertEqual(frame.getNbOfKnockedDownPins(3), 17)

    def test_get_throwing(self):
        """
        Tests if the get throwing method returns a tuple with all the throwing
        """
        frame = BowlingFrame("test")
        frame.registerThrowing(3)
        self.assertEqual(frame.getThrowing(), (3,))
        frame.registerThrowing(5)
        self.assertEqual(frame.getThrowing(), (3, 5))

    def test_get_throwing_ending(self):
        """
        Tests if the get throwing method returns a tuple with all the throwing, even in an ending frame
        """
        frame = BowlingFrame("test", ending=True)
        frame.registerThrowing(3)
        self.assertEqual(frame.getThrowing(), (3,))
        frame.registerThrowing(7)
        self.assertEqual(frame.getThrowing(), (3, 7))
        frame.registerThrowing(6)
        self.assertEqual(frame.getThrowing(), (3, 7, 6))

    def test_finish_hole(self):
        """
        Tests that the frame consider itself as finished after a hole
        """
        frame = BowlingFrame("test")
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(3)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(4)
        self.assertTrue(frame.isFinished)

    def test_finish_hole_ending(self):
        """
        Tests that an ending frame consider itself as finished after a hole on the two first throwing
        """
        frame = BowlingFrame("test", True)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(4)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(5)
        self.assertTrue(frame.isFinished)

    def test_finish_spare(self):
        """
        Tests that the frame consider itself as finished after a spare
        """
        frame = BowlingFrame("test")
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(3)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(7)
        self.assertTrue(frame.isFinished)

    def test_finish_spare_ending(self):
        """
        Tests that an ending frame does not consider itself as finished after a spare on the two first throwing
        """
        frame = BowlingFrame("test", True)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(3)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(7)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(4)
        self.assertTrue(frame.isFinished)

    def test_finish_spare_ending2(self):
        """
        Tests that an ending frame does not consider itself as finished after a spare on the two first throwing
        """
        frame = BowlingFrame("test", True)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(3)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(7)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(10)
        self.assertTrue(frame.isFinished)

    def test_finish_strike(self):
        """
        Tests that the frame consider itself as finished after a strike
        """
        frame = BowlingFrame("test")
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(10)
        self.assertTrue(frame.isFinished)

    def test_finish_strike_ending(self):
        """
        Tests that an ending frame does not consider itself as finished after a single strike on the two first throwing
        """
        frame = BowlingFrame("test", True)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(10)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(3)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(3)
        self.assertTrue(frame.isFinished)

    def test_finish_strike_ending2(self):
        """
        Tests that an ending frame does not consider itself as finished after two strikes on the two first throwing
        """
        frame = BowlingFrame("test", True)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(10)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(10)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(3)
        self.assertTrue(frame.isFinished)

    def test_finish_strike_ending3(self):
        """
        Tests that an ending frame does not consider itself as finished after three strikes on the two first throwing
        """
        frame = BowlingFrame("test", True)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(10)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(10)
        self.assertFalse(frame.isFinished)
        frame.registerThrowing(10)
        self.assertTrue(frame.isFinished)

    def test_is_hole(self):
        """
        Tests that the frame detects the hole
        """
        frame = BowlingFrame("test")
        self.assertFalse(frame.isHole() or frame.isSpare() or frame.isStrike())
        frame.registerThrowing(3)
        self.assertFalse(frame.isHole() or frame.isSpare() or frame.isStrike())
        frame.registerThrowing(4)
        self.assertTrue(frame.isHole())
        self.assertFalse(frame.isSpare() or frame.isStrike())

    def test_is_spare(self):
        """
        Tests that the frame detects the spare
        """
        frame = BowlingFrame("test")
        self.assertFalse(frame.isHole() or frame.isSpare() or frame.isStrike())
        frame.registerThrowing(6)
        self.assertFalse(frame.isHole() or frame.isSpare() or frame.isStrike())
        frame.registerThrowing(4)
        self.assertTrue(frame.isSpare())
        self.assertFalse(frame.isHole() or frame.isStrike())

    def test_is_strike(self):
        """
        Tests that the frame detects the strike
        """
        frame = BowlingFrame("test")
        self.assertFalse(frame.isHole() or frame.isSpare() or frame.isStrike())
        frame.registerThrowing(10)
        self.assertTrue(frame.isStrike())
        self.assertFalse(frame.isHole() or frame.isSpare())

    def test_score_hole(self):
        """
        Tests that the score of a frame is updated directly after the hole is finished
        """
        frame = BowlingFrame("test")
        self.assertTrue(frame.getScore() is None)
        frame.registerThrowing(4)
        self.assertTrue(frame.getScore() is None)
        frame.registerThrowing(5)
        self.assertEqual(frame.getScore(), 9)

    def test_previous_score_hole(self):
        """
        Tests that the score of a frame is updated directly after the hole is finished, taking into account the
        previous score
        """
        frame = BowlingFrame("test")
        self.assertTrue(frame.getScore() is None)
        frame.registerThrowing(4)
        self.assertTrue(frame.getScore() is None)
        frame.registerThrowing(5)
        self.assertEqual(frame.getScore(), 9)
        frame.setPreviousScore(10)
        self.assertEqual(frame.getScore(), 19)

    def test_score_spare(self):
        """
        Tests that the score of a frame is updated correctly after the spare and the 1st throwing of the next frame are
        finished
        """
        frame1 = BowlingFrame("test")
        frame2 = BowlingFrame("test")
        frame1.registerThrowing(9)
        frame1.registerThrowing(1)
        self.assertTrue(frame1.getScore() is None)
        frame2.registerThrowing(3)
        frame1.computeScore(frame2)
        self.assertEqual(frame1.getScore(), 13)
        self.assertTrue(frame2.getScore() is None)

    def test_score_spare2(self):
        """
        Tests that the score of a frame is updated correctly after the spare and the strike of the next frame are
        finished
        """
        frame1 = BowlingFrame("test")
        frame2 = BowlingFrame("test")
        frame1.registerThrowing(9)
        frame1.registerThrowing(1)
        self.assertTrue(frame1.getScore() is None)
        frame2.registerThrowing(10)
        frame1.computeScore(frame2)
        self.assertEqual(frame1.getScore(), 20)
        self.assertTrue(frame2.getScore() is None)

    def test_score_strike(self):
        """
        Tests that the score of a frame is updated correctly after a single strike
        """
        frame1 = BowlingFrame("test")
        frame2 = BowlingFrame("test")
        frame1.registerThrowing(10)
        self.assertTrue(frame1.getScore() is None)
        frame2.registerThrowing(2)
        self.assertTrue(frame1.getScore() is None)
        frame2.registerThrowing(5)
        frame1.computeScore(frame2)
        self.assertEqual(frame1.getScore(), 17)

    def test_score_strike2(self):
        """
        Tests that the score of a frame is updated correctly after two strikes in a row
        """
        frame1 = BowlingFrame("test")
        frame2 = BowlingFrame("test")
        frame3 = BowlingFrame("test")
        frame1.registerThrowing(10)
        self.assertTrue(frame1.getScore() is None)
        frame2.registerThrowing(10)
        self.assertTrue(frame1.getScore() is None)
        frame3.registerThrowing(4)
        frame1.computeScore(frame2, frame3)
        self.assertEqual(frame1.getScore(), 24)
        frame3.registerThrowing(4)
        frame2.computeScore(frame3)
        self.assertEqual(frame2.getScore(), 24 + 18)
        self.assertEqual(frame3.getScore(), 24 + 18 + 8)

    def test_score_strike3(self):
        """
        Tests that the score of a frame is updated correctly after three strikes in a row
        """
        frame1 = BowlingFrame("test")
        frame2 = BowlingFrame("test")
        frame3 = BowlingFrame("test")
        frame1.registerThrowing(10)
        self.assertTrue(frame1.getScore() is None)
        frame2.registerThrowing(10)
        self.assertTrue(frame1.getScore() is None)
        frame3.registerThrowing(10)
        frame1.computeScore(frame2, frame3)
        self.assertEqual(frame1.getScore(), 30)

    def test_too_much_pins_error(self):
        """
        Checks if the good error is raised when too much pins seem to have been knocked out
        """
        frame = BowlingFrame("test")
        self.assertRaises(PinsOverflowError, frame.registerThrowing, 19)
        frame.registerThrowing(9)
        self.assertRaises(PinsOverflowError, frame.registerThrowing, 3)

    def test_negative_pins_error(self):
        """
        Checks if the good error is raised when a negative number of pins is passed
        """
        frame = BowlingFrame("test")
        self.assertRaises(ValueError, frame.registerThrowing, -1)



