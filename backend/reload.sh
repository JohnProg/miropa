#!/usr/bin/env bash

pip install -r requirements.txt
sh loaddata.sh
python miropa/manage.py runserver


