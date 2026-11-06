import logging
import os
from redis import Redis
import requests
import time
import signal

DEBUG = os.environ.get("DEBUG", "").lower().startswith("y")

log = logging.getLogger(__name__)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)


redis = Redis("redis")

# Global flag used to request a graceful shutdown
STOP = False


def get_random_bytes():
    r = requests.get("http://rng/32")
    return r.content


def hash_bytes(data):
    r = requests.post(
        "http://hasher/",
        data=data,
        headers={"Content-Type": "application/octet-stream"},
    )
    hex_hash = r.text
    return hex_hash


def work_loop(interval=1):
    global STOP
    deadline = 0
    loops_done = 0
    while not STOP:
        if time.time() > deadline:
            log.info(
                "%s units of work done, updating hash counter",
                loops_done,
            )
            redis.incrby("hashes", loops_done)
            loops_done = 0
            deadline = time.time() + interval
        work_once()
        loops_done += 1


def work_once():
    log.debug("Doing one unit of work")
    time.sleep(0.1)
    random_bytes = get_random_bytes()
    hex_hash = hash_bytes(random_bytes)
    if not hex_hash.startswith("0"):
        log.debug("No coin found")
        return
    log.info("Coin found: %s...", hex_hash[:8])
    created = redis.hset("wallet", hex_hash, random_bytes)
    if not created:
        log.info("We already had that coin")


def handle_sigterm(signum, frame):
    global STOP
    # Request a graceful shutdown on SIGTERM/SIGINT
    log.info("Received signal %s, requesting shutdown", signum)
    STOP = True


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigterm)

    while not STOP:
        try:
            work_loop()
        except Exception:
            if STOP:
                # We are shutting down, stop restarting the loop
                break
            log.exception("In work loop:")
            log.error("Waiting 10s and restarting.")
            time.sleep(10)

    log.info("Worker exiting")

