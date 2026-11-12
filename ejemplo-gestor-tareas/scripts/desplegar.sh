#!/usr/bin/env bash
# Despliega la imagen IMAGEN:IMAGE_TAG con Docker Compose en esta máquina.
# Si la nueva versión no pasa el health check, vuelve a la última versión buena.
set -euo pipefail

: "${PROYECTO:?Falta PROYECTO}"
: "${IMAGEN:?Falta IMAGEN}"
: "${IMAGE_TAG:?Falta IMAGE_TAG}"
COMPOSE="docker compose -p ${PROYECTO} -f compose.prod.yaml"
URL_SALUD="${URL_SALUD:-http://localhost:8000/health}"
ESTADO_DIR="${HOME}/.despliegues/${PROYECTO}"
mkdir -p "${ESTADO_DIR}"
ANTERIOR="$(cat "${ESTADO_DIR}/ultimo_ok" 2>/dev/null || true)"

export IMAGEN IMAGE_TAG
echo "▶ Desplegando ${IMAGEN}:${IMAGE_TAG} (anterior: ${ANTERIOR:-ninguna})"

${COMPOSE} pull
${COMPOSE} up -d --remove-orphans

echo "▶ Esperando a que la aplicación responda en ${URL_SALUD}"
for intento in $(seq 1 30); do
  if curl -fsS --max-time 3 "${URL_SALUD}" > /dev/null; then
    echo "✅ Versión ${IMAGE_TAG} en línea (intento ${intento})"
    echo "${IMAGE_TAG}" > "${ESTADO_DIR}/ultimo_ok"
    docker image prune -f > /dev/null
    exit 0
  fi
  sleep 2
done

echo "❌ La versión ${IMAGE_TAG} no respondió."
${COMPOSE} logs --tail 50 || true
if [ -n "${ANTERIOR}" ]; then
  echo "↩ Rollback a ${ANTERIOR}"
  IMAGE_TAG="${ANTERIOR}" ${COMPOSE} up -d --remove-orphans
fi
exit 1
