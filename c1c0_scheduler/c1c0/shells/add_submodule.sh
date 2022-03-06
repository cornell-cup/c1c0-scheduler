#!/bin/bash

read -p "Please enter the name of the submodule: " userin
python3 -m venv "${userin}_venv"
touch "start_${userin}.py"
echo "# Please enter startup code here." > "start_${userin}.py"
echo
echo "Please edit start_${userin}.py to specify how your submodule functions."
