#!/usr/bin/env python2.7
# Created by Sam Gleske
# MIT License
# Pop!_OS 18.04 LTS
# Linux 5.4.0-65-generic x86_64
# Python 2.7.17

# This is a simple Python script meant to read a BabyTime data export and
# convert it into JSON Array time series data.  The end goal is to push these
# metrics into a time series database for richer dashboards like Grafana.

import json
import os
import re
import sys

def get_type(record):
    entries = [line.strip() for line in record.split('\n')]
    for entry in entries:
        if entry.split(':')[0].strip() == "Type":
            return entry.split(':')[1].strip()
    raise Exception("There's a bug because this exception shouldn't be thrown.")

def entry_touple(entry):
    legend = {
        "Type": "event",
        "Duration": "duration_min",
        "Pumping Left": "pump_left_breast_min",
        "Pumping Right": "pump_right_breast_min",
        "Pumping Total Amount(ml)": "pump_total_ml",
        "Pumping Left Amount(ml)": "pump_left_breast_ml",
        "Pumping Right Amount(ml)": "pump_right_breast_ml",
        "Formula Total Amount(ml)": "feed_formula_ml",
        "Breastfeeding Left": "feed_breast_left_min",
        "Breastfeeding Right": "feed_breast_right_min",
        "Etc title": "etc_title",
        "Pumped Milk Total Amount(ml)": "feed_pump_ml",
        "Diaper type": "diaper_type",
        "Pumped Milk Total Duration": "feed_pump_min",
        "Memo": "notes",
        "Poop Color": "poop_color"
    }
    e = [x.strip() for x in entry.split(':')]
    if e[0] not in legend:
        raise Exception('Unknown record %s' % e[0])
    e[0] = legend[e[0]]
    if '(min)' in e[1] or '(ml)' in e[1]:
        e[1] = int(re.findall(r'\d+', e[1])[0])
    return e

def process_record(record):
    entries = [line.strip() for line in record.split('\n')]
    metric = {}
    # get time
    if '~' in entries[0]:
        metric['time'] = entries[0].split('~')[0].strip()
    else:
        metric['time'] = entries[0]
    if os.getenv('TZ') is not None:
        metric['time'] = ' '.join([metric['time'], os.getenv('TZ')])
    # data
    for (x, y) in map(entry_touple, entries[1:]):
        metric[x] = y
    # update metric types
    if 'Breastfeeding' in metric['event']:
        metric['event'] = 'Breastfeeding'
    elif metric['event'] == 'Pee':
        metric['event'] = 'Change Diaper'
    elif metric['event'] == 'Pumped Milk':
        metric['event'] = 'Feed Pumped Milk'
    elif metric['event'] == 'Formula':
        metric['event'] = 'Feed Formula'
    # diaper metrics
    if metric['event'] == 'Change Diaper' and metric['diaper_type'] in ('Pee', 'Both'):
        metric['pee'] = True
    if metric['event'] == 'Change Diaper' and metric['diaper_type'] in ('Poop', 'Both'):
        metric['poop'] = True

    # memo processing for richer data
    if 'etc_title' in metric:
        if 'Spit Up' in metric['etc_title']:
            metric['spit_up'] = True
        if 'tongue lift' in metric['etc_title']:
            metric['tongue_lift'] = True
    if 'notes' in metric:
        if 'Spit Up' in metric['notes']:
            metric['spit_up'] = True
        if 'Yellow Nipple' in metric['notes']:
            metric['yellow_nipple'] = True
        if 'Purple Nipple' in metric['notes']:
            metric['purple_nipple'] = True
    return metric


filter_records = ["Hospital", "Temperature"]
with open(sys.argv[1], 'r') as f:
    doc = f.read()

re.split(r'===+', doc)
#records = doc.split('='*20)
records = re.split(r'===+', doc)
records = [record.strip() for record in records]
records = filter(lambda x: len(x) > 0 and get_type(x) not in filter_records, records)

metrics = map(process_record, records)
print(json.dumps(metrics, indent=4, separators=(',', ': '), sort_keys=True))
