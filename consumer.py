from kafka import KafkaConsumer
from datetime import datetime
import csv, yaml, sys
import pandas as pd
from analysis import forecast

# kafka_server = sys.argv[1]
consumer = KafkaConsumer(bootstrap_servers='192.168.1.7:9092')
consumer.subscribe(['metrics-2'])

columns = ['ds']

for msg in consumer:
	data = yaml.safe_load(msg.value.decode('utf-8'))
	if(data):
		for metric in data:
			columns.append(metric['metric']['pod'])
	break

df = pd.DataFrame(columns=columns)

count = 0
for msg in consumer:
	count = count + 1
	data = yaml.safe_load(msg.value.decode('utf-8'))
	if(data):
		row = []
		row.append(datetime.fromtimestamp(data[0]['value'][0]))
		for metric in data:
			memory = metric['value'][1]
			row.append(memory)
		df = df.append(pd.DataFrame([row], columns=columns))
	if(count==120):
		count = count-60
		forecast(df.set_index('ds'))
		