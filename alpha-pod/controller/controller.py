from kubernetes import config, client, watch
import yaml 
from kafka import KafkaConsumer
import os 
from prometheus_api_client import PrometheusConnect
from math import ceil
import sys

KAFKA_IP = sys.argv[1]
PROMETHEUS_SERVER = sys.argv[2]
QUERY = sys.argv[3]
RATIO = float(sys.argv[4])

prometheus = PrometheusConnect(url=PROMETHEUS_SERVER, disable_ssl=True)

consumer = KafkaConsumer(bootstrap_servers=KAFKA_IP,
						 auto_offset_reset='earliest')

query_res = prometheus.custom_query(query=QUERY)

memory_limit = query_res[0]['value'][1]
memory_limit = RATIO*float(memory_limit)

consumer.subscribe(['predictions'])

for msg in consumer:
	data = yaml.safe_load(msg.value.decode('utf-8'))
	max_utilisation = max(data['predictions'])
	scale_size = ceil(max_utilisation/memory_limit)
	if(scale_size>1):
		os.system(f'kubectl scale --replicas={scale_size} -n monitoring deployments/prometheus')