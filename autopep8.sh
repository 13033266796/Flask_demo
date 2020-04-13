#!/bin/sh

PYTHONPATH=. autopep8 --in-place -v -r ./monarch
PYTHONPATH=. autopep8 --in-place -v -r ./tests
