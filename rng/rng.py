from flask import Flask, Response
import os
import socket
import time

app = Flask(__name__)

app.debug = os.environ.get("DEBUG", "").lower().startswith("y")

hostname = socket.gethostname()
urandom = os.open("/dev/urandom", os.O_RDONLY)


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
    # IMPORTANT: écoute sur IPv4 uniquement pour K8s/Rancher
    app.run(host="0.0.0.0", port=port)
