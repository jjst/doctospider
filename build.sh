#!/bin/sh

mkdir -p ./build
cp *.py ./build/
pip3 install --target ./build -r ./requirements.txt
cd build
zip -m -r lambda.zip .

# Cleanup
