#!/bin/sh
set -e

echo "Running migrations..."
uv run alembic upgrade head

echo "Starting app..."
uv run python -m src.main