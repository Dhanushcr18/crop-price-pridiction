#!/usr/bin/env bash
set -e

case "$1" in
  data)
    python -m src.data.pipeline
    ;;
  train)
    python -m src.models.forecast
    ;;
  eval)
    python -m src.evaluation.evaluate
    ;;
  test)
    pytest -v
    ;;
  app)
    streamlit run app.py
    ;;
  all)
    python -m src.data.pipeline
    python -m src.models.forecast
    python -m src.evaluation.evaluate
    pytest -v
    ;;
  *)
    echo "Usage: $0 {data|train|eval|test|app|all}"
    exit 1
    ;;
esac

