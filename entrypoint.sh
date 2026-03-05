#!/bin/bash
set -e

echo "Running migrations..."
/app/.venv/bin/alembic upgrade head

echo "Starting app..."
uv run python -m src.main