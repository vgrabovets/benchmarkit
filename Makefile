lint:
	flake8 --show-source benchmarkit
	isort --check-only -rc benchmarkit --diff

	flake8 --show-source setup.py
	isort --check-only setup.py --diff

	flake8 --show-source tests
	isort --check-only -rc tests --diff

test:
	pytest tests

install_dev:
	pip install -r requirements/prod.txt
	pip install -r requirements/dev.txt
	pip install -e .
