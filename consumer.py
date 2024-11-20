from kafka import KafkaConsumer
from river import preprocessing, compose
import numpy as np

# Kafka consumer setup
consumer = KafkaConsumer('image_topic', bootstrap_servers='localhost:9092')

# Preprocessing pipeline for image classification (example: using standard scaler)
preprocessor = compose.TransformerUnion(
    preprocessing.StandardScaler()
)

# Classifier (example: using Naive Bayes from River)
from river import naive_bayes

# TODO: CHANGE THIS NAIVE BAYES CLASSIFIER WITH RESNET FROM PYTLARZ ET AL.
model = naive_bayes.GaussianNB()

# Consume messages and classify images
for msg in consumer:
    # Assume msg.value is the image data (you might need to decode or process it)
    image_data = np.frombuffer(msg.value, dtype=np.uint8)  # Example: convert to numpy array
    # Preprocess image data (example: scale)
    preprocessed_data = preprocessor.transform_one(image_data)
    # Predict using the model
    y_pred = model.predict_one(preprocessed_data)
    print(f"Image classified as: {y_pred}")

