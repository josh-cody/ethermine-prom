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

timeGauge = Gauge('time', 'the time', ["workerid"])
reportedHashrateGauge = Gauge('reported_hashrate', 'the reported hashrate', ["workerid"])
currentHashrateGauge = Gauge('current_hashrate', 'the current hashrate', ["workerid"])
validSharesGauge = Gauge('valid_shares', 'the number of valid shares', ["workerid"])
invalidSharesGauge = Gauge('invalid_shares', 'the number of invalid shares', ["workerid"])
staleSharesGauge = Gauge('stale_shares', 'the number of stale shares', ["workerid"])
activeWorkersGauge = Gauge('active_workers', 'the number of active workers', ["workerid"])

while True:
    for i in apiCall:
        
        dat = requests.get(i)
        jsonDat = json.loads(dat.text)
        dat2 = jsonDat["data"]
        rawData = dat2["statistics"]
        for j in rawData:
            timeGauge.labels(workerIDs[apiCall.index(i)]).set(j['time'])
            reportedHashrateGauge.labels(workerIDs[apiCall.index(i)]).set(j['reportedHashrate'])
            currentHashrateGauge.labels(workerIDs[apiCall.index(i)]).set(j['currentHashrate'])
            validSharesGauge.labels(workerIDs[apiCall.index(i)]).set(j['validShares'])
            invalidSharesGauge.labels(workerIDs[apiCall.index(i)]).set(j['invalidShares'])
            staleSharesGauge.labels(workerIDs[apiCall.index(i)]).set(j['staleShares'])
            activeWorkersGauge.labels(workerIDs[apiCall.index(i)]).set(j['activeWorkers'])
    time.sleep(int(config['info']['scrape_interval']))
