#!/usr/bin/env bash

echo ">> Removing dist/ directory"
rm -rf dist

echo ">> Running pysintaller"
pyinstaller --name FeatureRanking --onefile -y  \
    --additional-hooks-dir=. "Z:/src/main/python/fearank/main.py" \
	--hidden-import sklearn \
	--hidden-import sklearn.neighbors.typedefs \
	--hidden-import sklearn.neighbors.quad_tree \
	--hidden-import sklearn.tree._utils \
	--hidden-import pandas \
	--icon "Z:/src/main/icons/Icon.ico"

echo ">> Copying Icon.ico to dist"
cp src\\main\\icons\\Icon.ico dist\\
