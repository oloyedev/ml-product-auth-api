from flask import Flask, render_template, request, send_file
import numpy as np
import cv2
import io
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)

# Load the YOLO model
model = YOLO('best.pt')

# Allowed extensions for file upload
extensions = {'png', 'jpg', 'jpeg', 'gif'}

# Mapping of class IDs to class names
class_map = {
    0: 'Amstel Malt Bottle',
    1: 'Amstel Malt Can',
    2: 'Desperados',
    3: 'Heineken'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def predict_on_image(image_stream):
    image = Image.open(image_stream).convert('RGB')
    open_cv_image = np.array(image) 
    image = open_cv_image[:, :, ::-1].copy() 

    results = model.predict(image, conf=0.5)

    predictions = []
    for r in results:
        if r.boxes:  # Check if there are any boxes detected
            for box in r.boxes:
                class_id = int(box.cls.item())  # Convert tensor to int
                confidence = float(box.conf.item())  # Convert tensor to float
                class_name = class_map.get(class_id, "Unknown")
                predictions.append((class_name, confidence))
                
                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if not predictions:
        predictions.append(("Not our product", 0))

    # Convert annotated image back to PIL format
    annotated_image = Image.fromarray(image[:, :, ::-1])

    return predictions, annotated_image

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file and allowed_file(file.filename):
            file_data = file.read()
            file_stream = io.BytesIO(file_data)
            predictions, annotated_image = predict_on_image(file_stream)

            annotated_img_io = io.BytesIO()
            annotated_image.save(annotated_img_io, 'PNG')
            annotated_img_io.seek(0)

            return render_template(
                'result.html', 
                predictions=predictions, 
                image_data=file_data.decode('latin1'), 
                annotated_image_data=annotated_img_io.getvalue().decode('latin1')
            )

    return render_template('index.html')

@app.route('/display_image')
def display_image():
    image_data = request.args.get('image_data').encode('latin1')
    return send_file(io.BytesIO(image_data), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
