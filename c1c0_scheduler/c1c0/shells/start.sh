#!/bin/bash
submodule="$1";
shift;
echo "$PWD"
echo "./c1c0_scheduler/c1c0/shells/$submodule";
source "./c1c0_scheduler/c1c0/shells/$submodule"_venv/bin/activate;
python "./c1c0_scheduler/c1c0/shells/start_$submodule.py" $@;
# Note: args get passed forward!
# Perhaps later do
#python -m $SUBMODULE $@