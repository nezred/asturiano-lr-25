#!/bin/bash

#cd ${BASH_SOURCE}
COMPOSE=podman-compose
#COMPOSE=docker-compose
die() {
  printf '%s\n' "$1" >&2
  exit 1
}

genposdata() { (
  cd datproc || die 'FATAL ERROR'
  "$COMPOSE" down || die 'Error running '"$COMPOSE"' down'
  "$COMPOSE" up --build || die "Error running $COMPOSE up --build"
); }

[ -f ./out/wiki10_pos-full.json ] || genposdata

# install venv with requirements (dont bother with docker here)
