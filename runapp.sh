#!/bin/sh

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_HOST=shpe.uci.edu

flask run
