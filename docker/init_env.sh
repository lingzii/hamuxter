#!/bin/bash

set -e

python -m pip install --no-cache-dir -r server/requirements.txt

docker build -t hamuxter . --no-cache

docker-compose up -d --no-cache