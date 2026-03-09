#!/bin/bash
set -e

export NODE_PATH=/home/node/.node_modules
npm install #--prefix /home/node/.node_modules
exec "$@"