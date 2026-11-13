.PHONY: all data train eval test app web clean audit-trace

all: data train eval

data:
	python -m src.data.pipeline

audit-trace:
	python scripts/audit_trace.py

import-ksamb:
	python -m src.ingest.connectors.ksamb_pdf --file $(FILE)

train:
	python -m src.models.forecast

eval:
	python -m src.evaluation.evaluate

test:
	pytest -v

app:
	streamlit run app.py

web:
	python run.py web

clean:
	rm -rf __pycache__ .pytest_cache data/processed models/*.pkl

