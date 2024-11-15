#!/bin/bash
python main.py --team BLACK --name VikingAI --ip localhost --timeout $1 & \
python main.py --team WHITE --name VikingAI --ip localhost --timeout $1

