FROM python:3.12-alpine

WORKDIR /app

# Системные библиотеки
RUN apk add --no-cache \
    gobject-introspection \
    py3-gobject3 \
    libffi \
    pango \
    cairo \
    librsvg \
    fontconfig \
    ttf-dejavu \
    bash \
    build-base \
    libpq \
    postgresql-dev \
    git \
    curl

# Установка Poetry и UV
RUN pip install --no-cache-dir poetry uv

# Сначала копируем файлы pyproject.toml и README.md
COPY pyproject.toml README.md ./

# Выполняем uv sync (он должен видеть pyproject.toml)
RUN uv sync --no-dev

# Копируем весь проект
COPY . .

# Скрипт entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Настройки окружения
ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uv", "run", "python", "-m", "src.main"]