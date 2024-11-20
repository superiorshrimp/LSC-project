import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    key_serializer=lambda x: json.dumps(x).encode('utf-8'),
    value_serializer=lambda x: x
)

# Folder to monitor where the pathologists will dump their images
folder_to_watch = './data'

# Event handler for new files
class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            send_image_to_kafka(file_path)

# Function to extract label from the filename
def extract_label_from_filename(filename):
    """
    We assume that the label is part of the file name,
    'setosa_1.png' -> label: 'setosa'.
    """
    base_name = os.path.basename(filename)
    label = base_name.split('_')[0]
    return label

def send_image_to_kafka(file_path):
    label = extract_label_from_filename(file_path)
    with open(file_path, 'rb') as f:
        image_data = f.read()
        producer.send(
            'image_topic',
            key={"label": label},
            value=image_data
        )
        print(f"Produced image {file_path} with label '{label}' and sent to Kafka")

# Start monitoring folder for new files
observer = Observer()
observer.schedule(NewFileHandler(), path=folder_to_watch, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)  # Keep the observer thread running
except KeyboardInterrupt:
    observer.stop()

observer.join()

# Close Kafka producer
producer.close()
