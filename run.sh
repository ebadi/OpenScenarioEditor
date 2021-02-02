#!/bin/bash
if [ ! -d "pyesmini" ]
then
    git clone https://github.com/ebadi/pyesmini pyesmini
    cd pyesmini ; ./build.sh
    cd ..
fi
python3 OpenScenarioEditor.py
