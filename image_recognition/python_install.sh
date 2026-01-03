#!/bin/env bash
export PYTHONUNBUFFERED=1
python3 -m pip install -r image_recognition/requirements.txt
python3 -u image_recognition/kafka_connection.py