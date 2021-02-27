#!/bin/sh

mkdir -p ./build
cp *.py ./build/
pip install --target ./build -r ./requirements.txt
cd build
zip -m -r lambda.zip .

# Cleanup
