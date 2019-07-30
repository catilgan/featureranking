#!/usr/bin/env bash

echo "Activate pipenv environment"
pipenv shell

echo "Converting MainWindow.ui to MainWindow.py"
pyuic5 src/main/python/fearank/ui/MainWindow.ui > src/main/python/fearank/ui/MainWindow.py
