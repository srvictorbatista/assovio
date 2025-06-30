#!/bin/bash
set -e

MODEL_NAME="${MODEL_NAME:-vosk-model-small-pt-0.3}"
MODEL_DIR="modelos/$MODEL_NAME"
MODEL_ZIP="${MODEL_NAME}.zip"
MODEL_URL="https://alphacephei.com/vosk/models/${MODEL_ZIP}"

if [ ! -d "$MODEL_DIR" ]; then
  echo "[INFO] Modelo não encontrado. Iniciando download e extração..."

  mkdir -p modelos
  cd modelos

  if [ ! -f "$MODEL_ZIP" ]; then
    echo "[INFO] Baixando $MODEL_ZIP..."
    wget "$MODEL_URL"
  fi

  echo "[INFO] Extraindo $MODEL_ZIP..."
  unzip -n "$MODEL_ZIP"

  echo "[INFO] Removendo $MODEL_ZIP..."
  rm "$MODEL_ZIP"

  cd ..
else
  echo "[INFO] Modelo já presente em $MODEL_DIR. Pulando download."
fi

PORT="${INTERNAL_PORT:-5000}"
WORKERS="${WORKERS:-4}"
THREADS="${THREADS:-2}"

echo "[INFO] Iniciando servidor Gunicorn em 0.0.0.0:$PORT com $WORKERS workers e $THREADS threads..."
exec gunicorn --workers=$WORKERS --threads=$THREADS --bind 0.0.0.0:$PORT app:app
