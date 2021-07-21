import time
from kafka import KafkaProducer
import sys 
from prometheus_api_client import PrometheusConnect

KAFKA_IP = sys.argv[1]
PROMETHEUS_SERVER = sys.argv[2]
QUERY = sys.argv[3]
FREQ = int(sys.argv[4])


#Connect Producer client to the KAFKA server
client_producer = KafkaProducer(bootstrap_servers=KAFKA_IP)
#Connect to the Prometheus server in the K8s cluster
prometheus = PrometheusConnect(url=PROMETHEUS_SERVER, disable_ssl=True)

while(True):
    query_res = prometheus.custom_query(query=QUERY)
    query_res = bytes(str(query_res), 'utf-8')
    future = client_producer.send(f'metrics-{FREQ}', query_res)
    metadata = future.get(timeout=10)
    time.sleep(FREQ)
    
