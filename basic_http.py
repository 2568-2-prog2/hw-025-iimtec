import socket
import json
from config import HOST, PORT, ENDPOINT
from dice_api import roll_weighted_dice, validate_probabilities, parse_http_request, build_http_response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    try:
        request = client_socket.recv(4096).decode("utf-8")
        method, path, headers, body = parse_http_request(request)

        if method == "POST" and path == ENDPOINT:
            try:
                payload = json.loads(body)
                probabilities = payload["probabilities"]
                number_of_random = payload["number_of_random"]
                results = roll_weighted_dice(probabilities, number_of_random)
                response_body = json.dumps({"status": "success", "results": results})
                response = build_http_response("200 OK", response_body)
            except (ValueError, KeyError, json.JSONDecodeError) as exc:
                response_body = json.dumps({"status": "error", "message": str(exc)})
                response = build_http_response("400 Bad Request", response_body)
        elif method == "GET" and path == "/myjson":
            response_body = json.dumps({"status": "success", "message": "Hello, KU!"})
            response = build_http_response("200 OK", response_body)
        elif method == "GET":
            response_body = "<html><body><h1>Hello, World!</h1></body></html>"
            response = build_http_response("200 OK", response_body, content_type="text/html")
        else:
            response_body = json.dumps({"status": "error", "message": "Method not allowed"})
            response = build_http_response("405 Method Not Allowed", response_body)

        client_socket.sendall(response.encode("utf-8"))
    finally:
        client_socket.close()