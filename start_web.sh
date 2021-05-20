#!/bin/bash

export PATH=$PATH:c/Users/steve/Anaconda3
export FLASK_APP="web.py"
export SECRET_KEY="5fa09lajas9008fasd3451387a0aec5d2fsaf"
export FLASK_ENV=development
python --version
python -m flask run
