.PHONY: run install venv test clean

run:
	python -m src.etl.pipeline

install:
	pip install -r requirements.txt

venv:
	python -m venv venv

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 
	find . -type f -name "*.pyc" -delete
	
