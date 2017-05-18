#!/bin/bash

printf "\n\nRunning the yarn install\n\n"

yarn install

printf "\n\nMoving the node_modules into the `static` directory\n\n"

mv node_modules static

printf "\n\nInstalling the project dependencies via pip\n\n"

pip install -r requirements.txt

printf "\n\nStarting the app\n\n"

python app.py -p 8900