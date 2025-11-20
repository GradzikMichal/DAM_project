#!/bin/env bash
export PYTHONUNBUFFERED=1
python3 -m pip install psycopg2-binary kafka-python
python3 -u python_code/db_kafka.py