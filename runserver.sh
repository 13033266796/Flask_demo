#!/bin/sh

PYTHONUNBUFFERED=true gunicorn -c gunicorn_config.py monarch.wsgi:application
