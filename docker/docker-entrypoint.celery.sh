#!/bin/bash
set -e
python -m pip install --upgrade pip
pip install -r requirements.txt
export PATH=$PATH:/home/django/.local/bin
mkdir -p /tmp/prometheus
rm -rf /tmp/prometheus/*
exec "$@"