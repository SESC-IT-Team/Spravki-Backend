#!/bin/sh
set -e

echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
python -m src.main