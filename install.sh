#!/bin/bash
sudo apt install python3 python3-venv python3-pip
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0

sudo cp bucam.service /lib/systemd/system/bucam.service
sudo systemctl daemon-reload
sudo systemctl enable bucam.service