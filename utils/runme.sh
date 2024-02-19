#!/bin/bash

usage()
{
  cat <<EOF
Usage: setup.sh [OPTIONS]
Options:
 [--help]
 [--run[=finder,draw,analysis]]
EOF
  exit $1
}

while :; do
  case $1 in
    --help) printf '%s\n' "$usage" ; break;;
    --run)  type="$1"; shift ; continue;;
    *) break;;
  esac
  shift
done

if [[ $type == "finder" ]]; then 
    run=find_boxes.py
elif [[ $type == "draw" ]]; then
    run=process_boxes.py
elif [[ $type == "analysis" ]]; then
    run=my_analysis.py
fi

python $run