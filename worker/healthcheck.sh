#!/bin/sh
set -eu

MODE="${1:-}"

REDIS_HOST=redis
REDIS_PORT=6379

log() {
  echo "[healthcheck] $*" >&2
}

check_process() {
  # check process with PD 1
  if ! kill -0 1 2>/dev/null; then
    log "main process (PID 1) not running"
    return 1
  fi
}

check_redis() {
  python - <<EOF
import os, sys
import redis

host = os.environ.get("REDIS_HOST", "$REDIS_HOST")
port = int(os.environ.get("REDIS_PORT", "$REDIS_PORT"))

try:
    r = redis.Redis(host=host, port=port)
    r.ping()
except Exception as e:
    print(f"[healthcheck] cannot connect to Redis at {host}:{port}: {e}", file=sys.stderr)
    sys.exit(1)
EOF
}

case "$MODE" in
  liveness)
    # Only check if the process is alive
    check_process
    ;;

  readiness)
    # Check process and redis availability
    check_process
    check_redis
    ;;

  *)
		log "Command used: $0 $@"
    log "usage: $0 {liveness|readiness}"
    exit 1
    ;;
esac
