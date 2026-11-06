from flask import Flask, Response
import os
import socket
import time
import signal
import sys

app = Flask(__name__)

app.debug = os.environ.get("DEBUG", "").lower().startswith("y")

hostname = socket.gethostname()
urandom = os.open("/dev/urandom", os.O_RDONLY)


def handle_sigterm(signum, frame):
    # Close resources and exit quickly on SIGTERM
    try:
        os.close(urandom)
    except OSError:
        pass
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)


@app.route("/")
def index():
    return f"RNG running on {hostname}\n"


@app.route("/<int:how_many_bytes>")
def rng(how_many_bytes):
    time.sleep(0.1)
    return Response(os.read(urandom, how_many_bytes),
                    content_type="application/octet-stream")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "80"))
    # IMPORTANT: listen on IPv4 only for K8s/Rancher
    app.run(host="0.0.0.0", port=port)
