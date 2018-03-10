#!/bin/sh

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
ROOT="$(dirname $SCRIPTPATH)"

CONT="${ROOT}/singularity/neuro_pytorch.simg"
SCRIPT="${ROOT}/src/graph.py"

export PYTHONPATH=$ROOT

singularity exec -B /mnt:/mnt $CONT $SCRIPT 
