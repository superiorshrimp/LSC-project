from kafka import KafkaConsumer
from river import preprocessing, naive_bayes, compose
import numpy as np
import json

consumer = KafkaConsumer(
    'image_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: x,
    key_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
)

preprocessor = compose.TransformerUnion(
    preprocessing.StandardScaler()
)

model = naive_bayes.GaussianNB()

def extract_features(image_data):
    """
    Converts the image to the set of features.
    """
    image_array = np.frombuffer(image_data, dtype=np.uint8)

    red_mean = image_array[::3].mean() if len(image_array) >= 3 else 0
    green_mean = image_array[1::3].mean() if len(image_array) >= 3 else 0
    blue_mean = image_array[2::3].mean() if len(image_array) >= 3 else 0
    return {"red_mean": red_mean, "green_mean": green_mean, "blue_mean": blue_mean}

for msg in consumer:
    image_data = msg.value
    label = msg.key.get("label") if msg.key else None

    if label is None:
        print("No label, skipping")
        continue

    features = extract_features(image_data)

    preprocessor.learn_one(features)
    features_scaled = preprocessor.transform_one(features)

    model.learn_one(features_scaled, label)
    y_pred = model.predict_one(features_scaled)

    print(f"Image classified as: {y_pred} (real class: {label})")

