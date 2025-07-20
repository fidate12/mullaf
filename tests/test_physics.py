import unittest
from pinball import main


class TestPhysics(unittest.TestCase):
    def test_update_ball(self):
        ball = main.Ball(x=0, y=0, vx=10, vy=0)
        main.update_ball(ball, 1.0)
        self.assertAlmostEqual(ball.x, 10)
        self.assertAlmostEqual(ball.vy, main.GRAVITY)
        self.assertAlmostEqual(ball.y, main.GRAVITY)


if __name__ == "__main__":
    unittest.main()
