import numpy as np
import tensorflow as tf 
import cv2

IMG_SIZE = 64  

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_frame(frame):
    """Resize and normalize frame for model."""
    frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    frame = np.expand_dims(frame, axis=0) / 255.0 
    return frame.astype(np.float32)

def classify_frame(frame):
    """Run inference on a frame and return the predicted ASL letter."""
    input_data = preprocess_frame(frame)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    class_index = np.argmax(output_data)  
    predicted_letter = chr(class_index + 65)
    return predicted_letter

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    letter = classify_frame(frame)

    cv2.putText(frame, f"Predicted: {letter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("ASL Classification", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()