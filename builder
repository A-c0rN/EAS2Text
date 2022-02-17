#!/bin/bash

rm -rf dist/
rm -rf EAS2Text.egg-info/
python3 -m build
python3 -m twine upload dist/*