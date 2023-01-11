#!/bin/bash

# source py3.10-wbd/bin/activate
# flask --app dashboard.py --debug run
# sudo nohup python app1c.py > log.txt 2>&1 &

# https://medium.com/coding-memo/backend-run-flask-in-background-with-gunicorn-3f1f4cffca8d
# gunicorn -w 1 -b 0.0.0.1:5001 dashboard:app --daemon

# close
# ps -ef | grep gunicorn
# kill -9 [id]