from kafka import KafkaConsumer
from datetime import datetime 
import csv
import yaml 
import sys

KAFKA_IP = sys.argv[1]

#Defining the consumer
consumer = KafkaConsumer(bootstrap_servers=KAFKA_IP, auto_offset_reset='earliest')

#Open file to write data into and define the column names
fields = ['ds', 'pod1']
with open('data/data_final.csv', 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(fields)

"""
	Each message in KAFKA will be of the format: 

	[metric1, metric2, ...]

	Sample metric:

	{'metric': {'__name__': 'container_memory_usage_bytes', 'container': 'prometheus', 
	'endpoint': 'https-metrics', 
	'id': '/kubepods/burstable/pod085810f1-f3d1-4f6f-8fb7-bfa2ad547fcd/173647626d789c18c05774', 
	'image': 'sha256:3313ec19d0295a049e0710450afe4ee9fe6aca507ac199d4b78a381f3c1aca8c', 'instance': '192.168.1.14:10250', 
	'job': 'kubelet', 'metrics_path': '/metrics/cadvisor', 'name': 'k8s_prometheus_prometheus-k8s-1_monitoring_085810f1-f3d1-4f6f-8fb7-bfa2ad547fcd_5', 
	'namespace': 'monitoring', 'node': 'node-2', 'pod': 'prometheus-k8s-1', 'service': 'kubelet'}, 
	'value': [1626192875.732, '431296512']} 

	The "value" key of the metric is an array with the the timestamp(in unix format) and metric value.
"""

def kafka_python_consumer():
	#Subscribe to the necessary topics (metrics in this case).
	consumer.subscribe(['metrics'])
	#Open File in append mode to append data. 
	csvfile = open('data/data_final.csv', 'a')
	csvwriter = csv.writer(csvfile)
	count = 0
	#Iterate through each message in the Kafka Topic and process it. 
	for msg in consumer:
		count = count + 1
		#Convert bytes to string format.
		data = yaml.safe_load(msg.value.decode('utf-8'))
		#Iterate through every metric in the message.
		if(data):
			row = []
			"""
			Extract the timestamp from the first metric.
			Timestamps are same for metrics in the same message.

			"""
			row.append(datetime.fromtimestamp(data[0]['value'][0]))
			for metric in data:
				memory = metric['value'][1]
				row.append(memory)
			csvwriter.writerow(row)
		if(count%1000 == 0):
			print(f"Processed {count} Messages")
	csvfile.close()
			
kafka_python_consumer()