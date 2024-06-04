from flask import Flask, render_template, request
import numpy as np
import cv2
import os
from ultralytics import YOLO

# Load your YOLO model
model = YOLO('best (1).pt')

# Allowed file extensions
extensions = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# Mapping class IDs to class names
class_map = {
    0: 'Amstel Malt Bottle',
    1: 'Amstel Malt Can',
    2: 'Desperados',
    3: 'Heineken'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def predict_on_image(image_stream):
    image = cv2.imdecode(np.asarray(bytearray(image_stream.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    results = model.predict(image, conf=0.5)

    predictions = []
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls.item())  # Convert tensor to int
            confidence = float(box.conf.item())  # Convert tensor to float
            class_name = class_map.get(class_id, "Unknown")
            predictions.append((class_name, confidence))

    return predictions

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file and allowed_file(file.filename):
            predictions = predict_on_image(file.stream)
            return render_template('result.html', predictions=predictions)

    return render_template('index.html')

if __name__ == "__main__":
    app.run()
from flask import Flask, render_template, request
import numpy as np
import cv2
import os
from ultralytics import YOLO

# Load your YOLO model
model = YOLO('best (1).pt')

# Allowed file extensions
extensions = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# Mapping class IDs to class names
class_map = {
    0: 'Amstel Malt Bottle',
    1: 'Amstel Malt Can',
    2: 'Desperados',
    3: 'Heineken'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def predict_on_image(image_stream):
    image = cv2.imdecode(np.asarray(bytearray(image_stream.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    results = model.predict(image, conf=0.5)

    predictions = []
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls.item())  # Convert tensor to int
            confidence = float(box.conf.item())  # Convert tensor to float
            class_name = class_map.get(class_id, "Unknown")
            predictions.append((class_name, confidence))

    return predictions

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file and allowed_file(file.filename):
            predictions = predict_on_image(file.stream)
            return render_template('result.html', predictions=predictions)

    return render_template('index.html')

if __name__ == "__main__":
    app.run()
