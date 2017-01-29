#!/bin/bash

if test -z "$HOST" ; then
  HOST=10.0.0.155
fi

if test -z "$PORT" ; then
  PORT=5000
fi

BASE_URL="http://${HOST}:${PORT}"

get() {
  curl "$BASE_URL$1"
}

post() {
  curl -H 'Content-Type: application/json' --data-binary "$2" "$BASE_URL$1"
}

get /
