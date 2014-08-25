#!/usr/bin/env bash
python miropa/manage.py syncdb
python miropa/manage.py schemamigration apps.people --initial
#python miropa/manage.py loaddata fixtures/categories.json
#python miropa/manage.py loaddata fixtures/materials.yaml