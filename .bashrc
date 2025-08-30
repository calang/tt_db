# local .bashrc additions for timetable db project

WD=$(pwd)

export PYTHONPATH=${WD}

[ "$CONDA_DEFAULT_ENV" = "ttdb" ] || conda activate ttdb
