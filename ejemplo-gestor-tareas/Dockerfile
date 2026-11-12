FROM python:3.12-slim

ARG APP_COMMIT=dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PORT=8000 \
    APP_COMMIT=${APP_COMMIT}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

RUN useradd --create-home appuser && mkdir -p /datos && chown appuser /datos
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import os, urllib.request as u; u.urlopen('http://localhost:%s/health' % os.environ['PORT'])" || exit 1

# Forma "shell" para que se expanda ${PORT} (Render define su propio PORT)
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 "tareas.app:create_app()"
