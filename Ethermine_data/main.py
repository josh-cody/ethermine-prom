import requests
from prometheus_client import Gauge, start_http_server
import time
import json
import yaml

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

timeGauge = Gauge('time', 'the time')
reportedHashrateGauge = Gauge('reported_hashrate', 'the reported hashrate')
currentHashrateGauge = Gauge('current_hashrate', 'the current hashrate')
validSharesGauge = Gauge('valid_shares', 'the number of valid shares')
invalidSharesGauge = Gauge('invalid_shares', 'the number of invalid shares')
staleSharesGauge = Gauge('stale_shares', 'the number of stale shares')
activeWorkersGauge = Gauge('active_workers', 'the number of active workers')

while True:
    for i in apiCall:
        dat = requests.get(i)
        jsonDat = json.loads(dat.text)
        dat2 = jsonDat["data"]
        rawData = dat2["statistics"]
        #stats = json.load(rawData)
        if len(rawData) > 0:
            print(rawData[0])
        j = 0
        for j in rawData:
            timeGauge.labels(workerIDs[apiCall.index(i)]).set(rawData[j]['time'])
            print("rawData[0] \n", rawData[0])
            reportedHashrateGauge.labels(workerIDs[apiCall.index(i)]).set(rawData[j]['reportedHashrate'])
            currentHashrateGauge.labels(workerIDs[apiCall.index(i)]).set(rawData[j]['currentHashrate'])
            validSharesGauge.labels(workerIDs[apiCall.index(i)]).set(rawData[j]['validShares'])
            invalidSharesGauge.labels(workerIDs[apiCall.index(i)]).set(rawData[j]['invalidShares'])
            staleSharesGauge.labels(workerIDs[apiCall.index(i)]).set(rawData[j]['staleShares'])
            activeWorkersGauge.labels(workerIDs[apiCall.index(i)]).set(rawData[j]['activeWorkers'])
            j += 1
    time.sleep(int(config['info']['scrape_interval']))
