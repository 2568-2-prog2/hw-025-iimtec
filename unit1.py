import unittest
import json
from dice_api import validate_probabilities, roll_weighted_dice, parse_http_request

class ProgrammingTest(unittest.TestCase):
    def test_validate_probabilities_accepts_valid_list(self):
        weights = [0.1, 0.2, 0.3, 0.1, 0.2, 0.1]
        self.assertEqual(validate_probabilities(weights), weights)

    def test_validate_probabilities_rejects_invalid_sum(self):
        invalid = [0.1, 0.2, 0.3, 0.1, 0.2, 0.15]
        with self.assertRaises(ValueError):
            validate_probabilities(invalid)

    def test_roll_weighted_dice_returns_correct_count(self):
        result = roll_weighted_dice([0.1, 0.2, 0.3, 0.1, 0.2, 0.1], 5)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(1 <= face <= 6 for face in result))

    def test_parse_http_request_reads_method_path_and_body(self):
        request_text = (
            "POST /roll_dice HTTP/1.1\r\n"
            "Host: localhost\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: 44\r\n"
            "\r\n"
            '{"probabilities": [0.1, 0.2, 0.3], "number_of_random": 1}'
        )
        method, path, headers, body = parse_http_request(request_text)
        self.assertEqual(method, "POST")
        self.assertEqual(path, "/roll_dice")
        self.assertEqual(headers["Host"], "localhost")
        self.assertTrue(body.startswith("{"))
        self.assertIn("probabilities", json.loads(body))

if __name__ == "__main__":
    unittest.main()