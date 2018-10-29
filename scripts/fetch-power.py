#!/usr/bin/env python

import redis
import sys
import json
import datetime
import time
from datetime import timedelta

from elasticsearch import Elasticsearch


import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()

# Load config
ADC_GAIN = 2/3

with open(sys.argv[1]) as f:
    config = json.load(f)

current_sensors = config['current_sensors']

# Instantiate elasticsearch / redis client

esClient = Elasticsearch(config['elasticsearch']['hosts'],verify_certs=False)
rClient = redis.Redis(config['redis']['host'],config['redis']['port'])

bulkDocs = []

lastPollingTimestamp = datetime.datetime.now()

while True:

    # Determine current timestamp and calculate duration since last polling
    currentPollingTimestamp = datetime.datetime.now()
    durationBetweenLastPolling = (currentPollingTimestamp - lastPollingTimestamp).total_seconds()

    # Read sensors and save power info to redis
    power = {}

    power['timestamp'] = currentPollingTimestamp.isoformat()
    power['duration_between_last_polling'] = durationBetweenLastPolling

    for i, current_sensor in enumerate(current_sensors):

        power_per_sensor = {}

        power_per_sensor['adc_reading'] = adc.read_adc(i, gain=ADC_GAIN)

        if power_per_sensor['adc_reading'] > 0:
            power_per_sensor['amps'] = current_sensor['adc_reading_per_amp_constant'] * power_per_sensor['adc_reading']
        else:
            power_per_sensor['amps'] = 0

        power_per_sensor['kwh'] = (current_sensor['volts_constant'] * power_per_sensor['amps']) / 1000

        power_per_sensor['watts_used'] = (power_per_sensor['kwh'] * 1000.00) * (durationBetweenLastPolling / 3600.00)

        power_per_sensor['sensor'] = {}
        power_per_sensor['sensor']['adc_channel'] = current_sensor['adc_channel']
        power_per_sensor['sensor']['adc_reading_per_amp_constant'] = current_sensor['adc_reading_per_amp_constant']
        power_per_sensor['sensor']['volts_constant'] = current_sensor['volts_constant']

        power['power_usage_' + str(i)] = power_per_sensor

    bulkDocs.append(power)

    print ('================================================================')
    print ('UPDATE REDIS')
    print ('================================================================')
    print (power)
    print ('----------------------------------------------------------------')
    print ('bulkDocsCount => ' + str(len(bulkDocs)))
    print ('durationBetweenLastPolling => ' + str(durationBetweenLastPolling))
    print ('----------------------------------------------------------------')

    rClient.set('power',json.dumps(power))
    lastPollingTimestamp = currentPollingTimestamp

    if len(bulkDocs) == config['elasticsearch']['bulk_post_count']:
        print ('================================================================')
        print ('UPDATE ELASTICSEARCH')
        print ('================================================================')
        for i, bulkDoc in enumerate(bulkDocs):
            print bulkDoc
            r = esClient.index(index=config['elasticsearch']['index'], doc_type=config['elasticsearch']['index'], body=bulkDoc)
            print(r)

        bulkDocs = []

    time.sleep(config['polling_interval_in_seconds'])
