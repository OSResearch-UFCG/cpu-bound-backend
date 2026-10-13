import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("PORT", "8080"))
WORKERS = int(os.environ.get("WORKERS", "1"))
DEFAULT_N = 50000


def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def count_primes(limit):
    total = 0
    for number in range(limit + 1):
        if is_prime(number):
            total += 1
    return total


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        n = int(query.get("n", [DEFAULT_N])[0])

        primes = count_primes(n)

        body = json.dumps({"n": n, "primes": primes}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"cpu-bound-backend ouvindo na porta {PORT} com {WORKERS} worker(s)")

# Cada worker é um processo (a GIL impede ganho com threads em código CPU-bound)
# aceitando conexões no mesmo socket.
for _ in range(WORKERS - 1):
    if os.fork() == 0:
        break
server.serve_forever()
