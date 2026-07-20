#!/usr/bin/env bash
# Corre toda la suite de tests unitarios (web_app + api_ingestor) dentro de
# los contenedores Docker ya levantados por docker-compose.
#
# Uso:
#   ./run_tests.sh
#
# Se debe correr y estar 100% en verde ANTES de mergear a main / redeployar
# a producción. Si algo falla, este script termina con código != 0.
set -euo pipefail

FALLO=0

echo "===================================================="
echo "  Instalando dependencias de test (si faltan)..."
echo "===================================================="
docker exec web_app      pip install --quiet -r requirements-test.txt
docker exec api_ingestor pip install --quiet -r requirements-test.txt

echo
echo "===================================================="
echo "  Tests: web_app"
echo "===================================================="
if ! docker exec web_app python -m pytest tests/ -v; then
    FALLO=1
fi

echo
echo "===================================================="
echo "  Tests: api_ingestor"
echo "===================================================="
if ! docker exec api_ingestor python -m pytest tests/ -v; then
    FALLO=1
fi

echo
if [ "$FALLO" -ne 0 ]; then
    echo "❌ Hay tests rotos. NO pasar a producción hasta corregirlos."
    exit 1
else
    echo "✅ Todos los tests pasaron. OK para deployar."
fi
