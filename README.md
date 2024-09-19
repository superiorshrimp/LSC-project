# Mobula, Kafka based 
Online learning classification framework for medical imaging

Sandbox for the machine learning oracle for medical imaging with online/incremental learning.
The framework assumes Docker container with orchestration by Docker Swarm or Kubernetes, asynchronous architecture run by Kafka messaging. 
If we take the case of brain tumor images classification from Pytlarz et al. the idea is that pathologists dump once in while images in a folder and this improves continuosly the classifier. 
Initially we will use the River library (Creme), which is a powerful tool for tasks that involve continuous learning from streaming data.
![alt text](https://github.com/alecrimi/mobula/blob/main/image1.jpg) 

Steps:

__1. Run Kafka deploying the container according to the docker-compose.yaml__

docker-compose up

__2. Install necessary libraries__

python -m pip install kafka-python river

__3. Run the Producer and comsumer in a asynchronous manner keeping active the watchdog in case new images are dumped in the folder__

python producer.py &

python consumer.py &
