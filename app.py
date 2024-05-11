from flask import Flask, render_template, request
import pickle
import numpy as np
from keras.preprocessing import image as preprocessing
from PIL import Image
import io

app = Flask(__name__)

# Load the machine learning model
with open(r'C:\Users\Dinesh\Desktop\MCA_Project\Lung_cancer_prediction.pkl', 'rb') as f:
    ml_model = pickle.load(f)

# Assuming you have defined class_names
class_names = ["Benign cases", "Malignant cases", "Normal cases"]

@app.route('/')
def Home():
    return render_template("Home.html")

@app.route("/", methods=["POST", "GET"])
def Prediction():
    return render_template('Predict.html')


@app.route("/Predict", methods=["POST", "GET"])
def Predict():
    if request.method == "POST":
        uploaded_file = request.files['image']

        if uploaded_file.filename == '':
            return render_template("Predict.html", prediction_text="Error: Please choose an image to predict")


        image = Image.open(io.BytesIO(uploaded_file.read()))

        if image.mode != 'RGB':
            image = image.convert('RGB')

        target_size = (256, 256)  # Set your desired dimensions here
        image = image.resize(target_size)

        # Convert the image to a numpy array
        image_array = preprocessing.img_to_array(image)

        # Perform any necessary processing on the image array
        scaled_img = np.expand_dims(image_array, axis=0)

        # Make predictions using the model
        pred = ml_model.predict(scaled_img)
        output = class_names[np.argmax(pred)]

        if output == "Benign cases":
            ans = "Benign cases"
        elif output == "Malignant cases":
            ans = "Malignant cases"
        else:
            ans = "Normal cases"

        return render_template("Predict.html", prediction_text=ans)
    return render_template('Predict.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8082)
