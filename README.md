# Product Authenticity Verification API

This project is a Flask-based backend API that verifies whether a given product image belongs to an original product manufactured by a specific company. It uses a trained YOLOv8 object detection model to classify products, verify authenticity, and respond with annotated images and confidence scores.

## ✅ What It Does

- Accepts an image of a product via a web interface  
- Uses a YOLOv8 model (`best.pt`) to detect and classify the product  
- Verifies if the product is **genuine** and **produced by the target company**  
- Returns a clear message such as:  
  > **"Yes, this product is an original Amstel Malt Bottle produced by XYZ company."**  
- If the product is unrecognized, it returns:  
  > **"This is not a verified product from our company."**

## 🧠 Supported Products

The model currently supports:

- Amstel Malt Bottle  
- Amstel Malt Can  
- Desperados  
- Heineken  

(You can extend this by retraining the model with additional classes.)

## 📦 Stack

- **Backend**: Flask  
- **Model**: YOLOv8 (`ultralytics`)  
- **Image Processing**: OpenCV, Pillow  
- **Frontend**: Jinja2 Templates (HTML)

## 🚀 Getting Started

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/product-auth-verification-api.git
cd product-auth-verification-api
```

### Step 2: Install Dependencies

```bash
pip install flask numpy opencv-python pillow ultralytics
```

Or install from a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Add Your Model

Place your trained YOLOv8 weights file in the root directory and rename it:

```
best.pt
```

> Ensure the model was trained on the expected product classes.

### Step 4: Run the App

```bash
python app.py
```

By default, the app will be available at:

```
http://127.0.0.1:5000
```

## 📷 Usage

1. Visit the web interface in your browser.
2. Upload an image of a product.
3. The model will run predictions and annotate the image.
4. If the product is recognized and verified:
   - ✅ A message like “Yes, this is an original product created by XYZ company” is returned.
5. If it’s not in the class list:
   - ❌ It shows “Not our product”.

## 📁 Project Structure

```
.
├── app.py
├── best.pt
├── templates/
│   ├── index.html
│   └── result.html
└── static/           # Optional: for CSS, JS, images
```

## 📤 Deployment Notes

This system is designed for local or on-site (LAN) deployment.

For production:

- Set `debug=False` in `app.py`
- Use HTTPS and a reverse proxy (e.g., Nginx or Apache)
- Limit file upload size and validate file types
- Deploy with Gunicorn for better performance:
  ```bash
  gunicorn app:app --bind 0.0.0.0:8000
  ```
- Implement logging and error tracking
- (Optional) Use Docker for containerization


---

**Built by Olatunji Olayide Nelson**  
*Verifying product authenticity through AI.*
