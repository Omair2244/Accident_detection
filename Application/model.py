import tensorflow as tf
import numpy as np
import cv2

def load_model():
    """Load the pre-trained model."""
    model = tf.keras.models.load_model('path_to_your_model.h5')  # Update with your model path
    return model

def predict_frame(model, frame):
    """Preprocess the frame and make a prediction."""
    # Resize the frame to match model input dimensions
    resized_frame = cv2.resize(frame, (224, 224))  # Adjust as per your model's input size
    normalized_frame = resized_frame / 255.0  # Normalize pixel values
    input_data = np.expand_dims(normalized_frame, axis=0)  # Add batch dimension

    # Make prediction
    prediction = model.predict(input_data)
    label = np.argmax(prediction)  # Adjust based on your model's output

    # Example logic for detecting an accident
    if label == 1:  # Assuming label 1 corresponds to "Accident"
        return "Accident"
    else:
        return "No Accident"
