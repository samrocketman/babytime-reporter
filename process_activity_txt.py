#!/usr/bin/env python2.7

import json
import re
import sys

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
        "Breastfeeding Left": "feed_breast_left_ml",
        "Breastfeeding Right": "feed_breast_right_ml",
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
    if 'notes' in metric:
        if 'Spit Up' in metric['notes']:
            metric['spit_up'] = True
        if 'Yellow Nipple' in metric['notes']:
            metric['yellow_nipple'] = True
        if 'Purple Nipple' in metric['notes']:
            metric['purple_nipple'] = True
    return metric

with open(sys.argv[1], 'r') as f:
    doc = f.read()

re.split(r'===+', doc)
#records = doc.split('='*20)
records = re.split(r'===+', doc)
records = [record.strip() for record in records]
records = filter(lambda x: len(x) > 0, records)

metrics = map(process_record, records)
print(json.dumps(metrics, indent=4, separators=(',', ': '), sort_keys=True))
