FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    gobject-introspection \
    py3-gobject3 \
    libffi \
    pango \
    cairo \
    librsvg \
    fontconfig \
    ttf-dejavu


RUN pip install --no-cache-dir uv
COPY pyproject.toml README.md ./
RUN uv sync --no-dev

COPY . .

ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uv", "run", "python", "-m", "src.main"]
