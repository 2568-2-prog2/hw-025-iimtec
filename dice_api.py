import json
import random

def validate_probabilities(probabilities):
    if not isinstance(probabilities, list):
        raise ValueError("probabilities must be a list of 6 numbers")
    if len(probabilities) != 6:
        raise ValueError("probabilities must have 6 elements")
    if any(not isinstance(p, (int, float)) for p in probabilities):
        raise ValueError("probabilities must contain numeric values")
    if any(p < 0 or p > 1 for p in probabilities):
        raise ValueError("probabilities values must be between 0 and 1")
    total = sum(probabilities)
    if abs(total - 1.0) > 1e-9:
        raise ValueError("probabilities must sum to 1.0")
    return probabilities

def roll_weighted_dice(probabilities, number_of_random):
    validate_probabilities(probabilities)
    if not isinstance(number_of_random, int) or number_of_random <= 0:
        raise ValueError("number_of_random must be a positive integer")
    faces = [1, 2, 3, 4, 5, 6]
    return random.choices(faces, weights=probabilities, k=number_of_random)

def parse_http_request(request_text):
    lines = request_text.split("\r\n")
    request_line = lines[0].split()
    method = request_line[0]
    path = request_line[1]
    headers = {}
    i = 1
    while i < len(lines) and lines[i]:
        if ":" in lines[i]:
            key, value = lines[i].split(":", 1)
            headers[key.strip()] = value.strip()
        i += 1
    body = "\r\n".join(lines[i+1:]) if i + 1 < len(lines) else ""
    return method, path, headers, body

def build_http_response(status_line, body, content_type="application/json"):
    body_bytes = body.encode("utf-8")
    return (
        f"HTTP/1.1 {status_line}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"\r\n"
        f"{body}"
    )