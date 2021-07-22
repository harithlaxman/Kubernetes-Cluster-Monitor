# Kubernetes-Cluster-Monitor
### Framework to monitor, predict and scale K8s objects
The framework extracts container metrics (CPU usage, Memory Usage, etc.) via prometheus, streams it to an external Kafka server, analyses data at regular intervals of time and does a forecast for the required metric and send it back to the K8s cluster to apply policies to scale the application based on the forecast.
