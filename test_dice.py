import unittest
from dice import Dice

class TestDice(unittest.TestCase):

    def test_default_sides(self):
        d = Dice()
        self.assertEqual(d.sides, 6)

    def test_faces_correct(self):
        d = Dice(sides=4)
        self.assertEqual(d.faces, [1, 2, 3, 4])

    def test_uniform_probabilities(self):
        d = Dice(sides=4)
        for p in d.probabilities:
            self.assertAlmostEqual(p, 0.25)

    def test_custom_probabilities(self):
        probs = [0.1, 0.2, 0.3, 0.1, 0.2, 0.1]
        d = Dice(sides=6, probabilities=probs)
        self.assertEqual(d.probabilities, probs)

    def test_bad_prob_sum_raises(self):
        with self.assertRaises(ValueError):
            Dice(sides=3, probabilities=[0.5, 0.5, 0.5])

    def test_wrong_prob_length_raises(self):
        with self.assertRaises(ValueError):
            Dice(sides=6, probabilities=[0.5, 0.5])

    def test_roll_returns_int(self):
        d = Dice()
        self.assertIsInstance(d.roll(), int)

    def test_roll_in_range(self):
        d = Dice()
        for _ in range(100):
            self.assertIn(d.roll(), [1, 2, 3, 4, 5, 6])

    def test_roll_many_length(self):
        d = Dice()
        self.assertEqual(len(d.roll_many(10)), 10)

    def test_roll_many_values_in_range(self):
        d = Dice()
        for v in d.roll_many(100):
            self.assertIn(v, [1, 2, 3, 4, 5, 6])

    def test_deterministic_roll(self):
        d = Dice(sides=3, probabilities=[0.0, 0.0, 1.0])
        for _ in range(20):
            self.assertEqual(d.roll(), 3)

if __name__ == '__main__':
    unittest.main()
