# Mobula
Online learning classification framework for medical imaging

Sandbox for the machine learning oracle for medical imaging with online/incremental learning.
The framework assumes Docker container with orchestration by Docker Swarm or Kubernetes, asynchronous architecture run by Kafka messaging. 
If we take the case of brain tumor images classification from Pytlarz et al. the idea is that pathologists dump once in while images in a folder and this improves continuosly the classifier. 
Initially we will use the River library (Creme), which is a powerful tool for tasks that involve continuous learning from streaming data.
Steps:

**Run Kafka deploying the container according to the docker-compose.yaml **
docker-compose up

**Install necessary libraries **
python -m pip install kafka-python river

**Run the Producer and comsumer in a asynchronous manner keeping active the watchdog **
python producer.py &
python consumer.py &
