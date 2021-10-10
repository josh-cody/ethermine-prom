#!/usr/bin/python
import requests
from prometheus_client import Gauge, start_http_server
import time
import json
import yaml
import sys

def main(argv):
    with open("config.yaml", 'r') as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        if config:
            print("config file read sucessfully")
        else:
            print("error reading config file")

    start_http_server(config['info']['port'])
    workerIDs = []
    apiCall = []
    for j in config['info']['id']:
        workerIDs.append(j)
        apiCall.append("https://api.ethermine.org/miner/" + j + "/dashboard")

    timeGauge = Gauge('time', 'the time', ["workerid"])
    lastSeenGauge = Gauge('lastseen', 'last seen', ["workerid"])
    reportedHashrateGauge = Gauge('reported_hashrate', 'the reported hashrate', ["workerid"])
    unpaidGauge = Gauge('unpaid', 'unpaid value', ["workerid"])
    currentHashrateGauge = Gauge('current_hashrate', 'the current hashrate', ["workerid"])
    validSharesGauge = Gauge('valid_shares', 'the number of valid shares', ["workerid"])
    invalidSharesGauge = Gauge('invalid_shares', 'the number of invalid shares', ["workerid"])
    staleSharesGauge = Gauge('stale_shares', 'the number of stale shares', ["workerid"])
    activeWorkersGauge = Gauge('active_workers', 'the number of active workers', ["workerid"])


    dicts = {'time': timeGauge, 'lastSeen': lastSeenGauge, 'reportedHashrate': reportedHashrateGauge, 'unpaid': unpaidGauge, 'currentHashrate': currentHashrateGauge, 'validShares': validSharesGauge, 'invalidShares': invalidSharesGauge, 'staleShares': staleSharesGauge, 'activeWorkers': activeWorkersGauge}
    
    while True:
        for i in apiCall:
            
            dat = requests.get(i)
            jsonDat = json.loads(dat.text)
            dat2 = jsonDat["data"]
            rawData = dat2["currentStatistics"]
            print("updated")
            for j in rawData:
                dicts[j].labels(workerIDs[apiCall.index(i)]).set(rawData[j])
        time.sleep(int(config['info']['scrape_interval']))



if __name__ == "__main__":
    main(sys.argv[1:])
