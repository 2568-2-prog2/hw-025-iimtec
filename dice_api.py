import unittest
import json
import threading
import socket
import time
import requests

def start_server():
    from dice import Dice
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('localhost', 8082))
    srv.listen(5)
    srv.settimeout(5)
    while True:
        try:
            client_socket, _ = srv.accept()
        except socket.timeout:
            continue
        request = b""
        client_socket.settimeout(2)
        try:
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                request += chunk
        except socket.timeout:
            pass
        request = request.decode('utf-8')

        if request.startswith("GET /roll_dice"):
            body = request.split("\r\n\r\n", 1)[1].strip()
            payload = json.loads(body)
            probabilities = payload["probabilities"]
            n = payload["number_of_random"]
            dice = Dice(sides=len(probabilities), probabilities=probabilities)
            results = dice.roll_many(n)
            response_data = {"status": "success", "results": results}
            response_json = json.dumps(response_data)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{response_json}"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

t = threading.Thread(target=start_server, daemon=True)
t.start()
time.sleep(0.3)

class TestAPI(unittest.TestCase):

    def test_status_success(self):
        result = requests.get("http://localhost:8082/roll_dice", json={
            "probabilities": [1/6]*6,
            "number_of_random": 10
        }).json()
        self.assertEqual(result["status"], "success")

    def test_results_length(self):
        result = requests.get("http://localhost:8082/roll_dice", json={
            "probabilities": [1/6]*6,
            "number_of_random": 10
        }).json()
        self.assertEqual(len(result["results"]), 10)

    def test_results_values_in_range(self):
        result = requests.get("http://localhost:8082/roll_dice", json={
            "probabilities": [1/6]*6,
            "number_of_random": 60
        }).json()
        for v in result["results"]:
            self.assertIn(v, [1, 2, 3, 4, 5, 6])

    def test_biased_dice(self):
        result = requests.get("http://localhost:8082/roll_dice", json={
            "probabilities": [1, 0, 0, 0, 0, 0],
            "number_of_random": 20
        }).json()
        self.assertTrue(all(v == 1 for v in result["results"]))

    def test_four_sided_dice(self):
        result = requests.get("http://localhost:8082/roll_dice", json={
            "probabilities": [0.25, 0.25, 0.25, 0.25],
            "number_of_random": 20
        }).json()
        for v in result["results"]:
            self.assertIn(v, [1, 2, 3, 4])

if __name__ == '__main__':
    unittest.main()
