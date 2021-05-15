#!/bin/bash

# USAGE:
#     ./process_activity_txt.py *.txt | ./helper-scripts/get-strings.sh

jq '.[] | keys[]' |
  sort -u |
  grep -v '_ml"$\|_min"$\|^"pee"$\|^"poop"$\|^"spit_up"$\|^"purple_nipple"$\|^"yellow_nipple"$'
