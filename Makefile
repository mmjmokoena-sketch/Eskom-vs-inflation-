.PHONY: all run test demo site

all: run test

run:
	python -m src.run_all

test:
	pytest -q

demo:
	python -m src.run_all --mode synthetic

site:
	quarto render docs
