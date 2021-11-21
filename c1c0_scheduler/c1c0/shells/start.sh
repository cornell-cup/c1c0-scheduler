SUBMODULE=$1;
shift;
source $SUBMODULE/bin/activate
python start_$SUBMODULE.py $@
# Note: args get passed forward!
# Perhaps later do
#python -m $SUBMODULE $@