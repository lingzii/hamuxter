#!/bin/bash

set -e

uvicorn server.main:app --host 0.0.0.0 --port 8080 --reload