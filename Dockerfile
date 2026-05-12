FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache bash git

RUN pip install --no-cache-dir uv

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_TOOL_BIN_DIR=/usr/local/bin

COPY pyproject.toml ./

RUN uv sync --no-dev

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
EXPOSE 8000

CMD ["bash", "./entrypoint.sh"]