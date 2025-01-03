from kafka import KafkaConsumer
from deep_river.classification import RollingClassifier
from river import metrics, compose, preprocessing, datasets
import torch
from tqdm import tqdm
import numpy as np
import json

consumer = KafkaConsumer(
    'image_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: x,
    key_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
)

class RnnModule(torch.nn.Module):

    def __init__(self, n_features, hidden_size=1):
        super().__init__()
        self.n_features = n_features
        self.rnn = torch.nn.RNN(
            input_size=n_features, hidden_size=hidden_size, num_layers=1
        )
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, X, **kwargs):
        out, hn = self.rnn(X)  # lstm with input, hidden, and internal state
        hn = hn.view(-1, self.rnn.hidden_size)
        return self.softmax(hn)

model_pipeline = preprocessing.StandardScaler()
model_pipeline |= RollingClassifier(
    module=RnnModule,
    loss_fn="binary_cross_entropy_with_logits",
    optimizer_fn=torch.optim.SGD,
    window_size=20,
    lr=1e-2,
    append_predict=True,
    is_class_incremental=False,
)

metric = metrics.Accuracy()

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

    y_pred = model_pipeline.predict_one(features)  # make a prediction
    metric.update(label, y_pred)  # update the metric
    model_pipeline.learn_one(features, label)  # make the model learn

    print(f"Image classified as: {y_pred} (real class: {label})")
    print(f"Accuracy: {metric.get():.2f}")
'''
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
'''