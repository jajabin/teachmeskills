HERE := .
VENV := $(shell pipenv --venv)
SRC := ${HERE}/src
PYTHONPATH := ${SRC}

RUN := pipenv run
PY := ${RUN} python


.PHONY: format
format:
	${RUN} isort --virtual-env "${VENV}" --recursive --apply "${HERE}"
	${RUN} black "${HERE}"


.PHONY: run
run:
	${PY} src/manage.py runserver


.PHONY: migrate
migrate:
	${PY} src/manage.py migrate


.PHONY: migrations
migrations:
	${PY} src/manage.py makemigrations


.PHONY: su
su:
	${PY} src/manage.py createsuperuser