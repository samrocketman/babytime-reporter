#!/bin/bash

# DESCRIPTION:
#     I used this once to help me create JSON string entries for the
#     babytime-telegraf.conf file.  It felt like a waste not to share it.  Then
#     again, it's kind of a hack.

# USAGE:
#     ./process_activity_txt.py *.txt | ./helper-scripts/get-strings.sh

jq '.[] | keys[]' |
  sort -u |
  grep -v '_ml"$\|_min"$\|^"pee"$\|^"poop"$\|^"spit_up"$\|^"purple_nipple"$\|^"yellow_nipple"$'
