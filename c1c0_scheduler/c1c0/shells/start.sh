#!/bin/bash
submodule="$1";
shift;
echo "Running submodule from '$PWD'"
#echo "./c1c0_scheduler/c1c0/shells/$submodule";
source "./c1c0_scheduler/c1c0/shells/$submodule"_venv/bin/activate;
python "./c1c0_scheduler/c1c0/shells/start_$submodule.py" $@;
# Note: system/cmd args get passed forward! (That's what $@ means)
# Perhaps later we can use `python -m $SUBMODULE $@`