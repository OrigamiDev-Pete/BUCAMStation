#!/bin/bash
sudo apt install python3 python3-venv python3-pip

sudo cp bucam.service /lib/systemd/system/bucam.service
sudo systemctl daemon-reload
sudo systemctl enable bucam.service
