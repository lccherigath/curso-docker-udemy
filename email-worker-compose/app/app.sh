#!/bin/sh

pip install bottle==0.12.18 psycopg2==2.8.6 redis==3.5.3
python -u sender.py
