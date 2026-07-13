#!/bin/sh
# Two modes from one image:
#   serve-http        -> the Fly deployment: columna loopback-ungated + nginx public face
#   <anything else>   -> pass straight to columna-server (e.g. `demo --play` quickstart)
set -e

if [ "$1" = "serve-http" ]; then
  # ungated loopback (COLUMNA_MCP_TOKEN intentionally unset -> binds 127.0.0.1 only)
  columna-server demo --http 127.0.0.1:8765 &
  COLUMNA_PID=$!
  # give the MCP server a moment to bind before nginx starts proxying
  sleep 2
  # if columna died on startup, fail fast rather than serving a dead upstream
  if ! kill -0 "$COLUMNA_PID" 2>/dev/null; then
    echo "columna-server failed to start" >&2
    exit 1
  fi
  exec nginx -g 'daemon off;'
else
  exec columna-server "$@"
fi
