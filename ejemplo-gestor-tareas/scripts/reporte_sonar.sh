#!/usr/bin/env bash
# Genera REPORTE-CALIDAD.md con los datos de SonarQube (Cloud o Community Build).
# Uso:
#   SONAR_HOST=https://sonarcloud.io SONAR_PROJECT=usuario_repo SONAR_ORG=usuario ./scripts/reporte_sonar.sh
#   SONAR_HOST=http://localhost:9000 SONAR_PROJECT=gestor-tareas SONAR_TOKEN=xxx ./scripts/reporte_sonar.sh
# Requiere: curl y jq (sudo apt install jq | sudo dnf install jq | sudo pacman -S jq)
set -euo pipefail

: "${SONAR_HOST:=https://sonarcloud.io}"
: "${SONAR_PROJECT:?Define SONAR_PROJECT (project key)}"
SALIDA="${SALIDA:-REPORTE-CALIDAD.md}"
ORG_PARAM="${SONAR_ORG:+&organization=${SONAR_ORG}}"

api() {
  if [ -n "${SONAR_TOKEN:-}" ]; then
    curl -fsS -u "${SONAR_TOKEN}:" "${SONAR_HOST}/api/$1"
  else
    curl -fsS "${SONAR_HOST}/api/$1"
  fi
}

METRICAS="alert_status,ncloc,coverage,duplicated_lines_density,bugs,vulnerabilities,code_smells,security_hotspots,reliability_rating,security_rating,sqale_rating,sqale_index"

gate=$(api "qualitygates/project_status?projectKey=${SONAR_PROJECT}")
medidas=$(api "measures/component?component=${SONAR_PROJECT}&metricKeys=${METRICAS}")
issues=$(api "issues/search?componentKeys=${SONAR_PROJECT}&resolved=false&ps=50${ORG_PARAM}")
hotspots=$(api "hotspots/search?projectKey=${SONAR_PROJECT}&ps=1${ORG_PARAM}" || echo '{"paging":{"total":"?"}}')

m() { echo "${medidas}" | jq -r --arg k "$1" '.component.measures[] | select(.metric==$k) | .value' | head -n1 | grep . || echo '-'; }
nota() { case "${1%%.*}" in 1) echo A;; 2) echo B;; 3) echo C;; 4) echo D;; 5) echo E;; *) echo "-";; esac; }

{
  echo "# Reporte de calidad · ${SONAR_PROJECT}"
  echo
  echo "- Fecha: $(date '+%Y-%m-%d %H:%M')"
  echo "- Commit: \`$(git rev-parse --short HEAD 2>/dev/null || echo 'n/a')\`"
  echo "- Fuente: ${SONAR_HOST}"
  echo
  echo "## Quality Gate: **$(echo "${gate}" | jq -r '.projectStatus.status')**"
  echo
  echo "| Condición | Valor actual | Umbral | Estado |"
  echo "|---|---|---|---|"
  echo "${gate}" | jq -r '.projectStatus.conditions[]? | "| \(.metricKey) | \(.actualValue // "-") | \(.comparator) \(.errorThreshold) | \(.status) |"'
  echo
  echo "## Métricas generales"
  echo
  echo "| Métrica | Valor |"
  echo "|---|---|"
  echo "| Líneas de código | $(m ncloc) |"
  echo "| Cobertura | $(m coverage) % |"
  echo "| Duplicación | $(m duplicated_lines_density) % |"
  echo "| Bugs | $(m bugs) |"
  echo "| Vulnerabilidades | $(m vulnerabilities) |"
  echo "| Code smells | $(m code_smells) |"
  echo "| Security hotspots | $(m security_hotspots) (en revisión: $(echo "${hotspots}" | jq -r '.paging.total')) |"
  echo "| Calificación de fiabilidad | $(nota "$(m reliability_rating)") |"
  echo "| Calificación de seguridad | $(nota "$(m security_rating)") |"
  echo "| Calificación de mantenibilidad | $(nota "$(m sqale_rating)") |"
  echo "| Deuda técnica | $(m sqale_index) min |"
  echo
  echo "## Issues abiertos (máx. 50)"
  echo
  total=$(echo "${issues}" | jq -r '.total // .paging.total // 0')
  echo "Total: **${total}**"
  echo
  if [ "${total}" != "0" ]; then
    echo "| Severidad | Tipo | Archivo:línea | Mensaje |"
    echo "|---|---|---|---|"
    echo "${issues}" | jq -r '.issues[] | "| \(.severity // "-") | \(.type // "-") | \(.component | split(":") | last):\(.line // "-") | \(.message | gsub("\\|"; "/")) |"'
  fi
  echo
  echo "## Análisis y plan de acción"
  echo
  echo "_Completa esta sección a mano: qué significan los resultados, qué corregiste y qué queda pendiente._"
} > "${SALIDA}"

echo "Reporte generado en ${SALIDA}"
