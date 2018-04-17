#!/bin/bash

echo "check your python and pip version first"
python --version
pip --version

echo "Install dependences"

echo "Install slimit for AST"

sudo pip install slimit==0.8.1

echo "Install selenium for browser simulation"

sudo pip install selenium==3.6.0

sudo pip install tldextract