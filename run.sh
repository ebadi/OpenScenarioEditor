#!/bin/bash
if [ ! -d "pyesmini" ]
then
    sudo apt install git python3-pip python3-pyqt5 # first run, install missing packages
    pip3 install PyQt5
    git clone git@github.com:ebadi/pyesmini.git pyesmini  # dev repo
    cd pyesmini
    git checkout dev
    ./build.sh
    cd ..
fi
python3 OpenScenarioEditor.py
