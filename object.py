import cv2
import numpy as np
import importlib.util


# Paths to your configuration and weights files
weights_path = 'C:/Users/HEMA DARSHINY/Downloads/installation_opencv-python/object_detection/yolov4-tiny.weights'
config_path = 'C:/Users/HEMA DARSHINY/Downloads/installation_opencv-python/object_detection/yolov4-tiny.cfg'
names_path = 'C:/Users/HEMA DARSHINY/Downloads/installation_opencv-python/object_detection/coco.names'

# Load YOLO model
net = cv2.dnn.readNet(weights_path, config_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
with open(names_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Check loaded layers and class names
print("Layer names:", layer_names)
print("Number of layers:", len(layer_names))

# Initialize the video capture
cap = cv2.VideoCapture(0)  # Use 0 or 1 depending on your camera setup

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Function to open a new window (vol.py) to display detected labels
def open_vol_window(detected_labels):
    # Dynamically import vol.py to update it with the new labels
    spec = importlib.util.spec_from_file_location("vol", "vol.py")
    vol = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vol)
    
    # Pass detected labels to the vol.py window
    vol.display_labels(detected_labels)
    

# List to store detected labels
detected_labels = []

# Function to handle mouse click events
def mouse_click(event, x, y, flags, param):
    global stop_detection
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if the click is inside the "Done" rectangle at the bottom
        if 0 <= x <= frame.shape[1] and frame.shape[0] - 50 <= y <= frame.shape[0]:
            stop_detection = True  # Set stop_detection to True if clicked on the button-like rectangle
            print("Done button clicked.")
            

# Set up the OpenCV window to listen for mouse events
cv2.namedWindow("Detection")
cv2.setMouseCallback("Detection", mouse_click)

# Initialize stop_detection flag
stop_detection = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Print frame dimensions to ensure the frame is being captured correctly
    print("Frame dimensions: ", frame.shape)

    # Prepare the frame for YOLO input
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    # Post-process the results
    class_ids = []
    confidences = []
    boxes = []
    height, width, channels = frame.shape
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:  # Lower confidence threshold to 0.2
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w // 2
                y = center_y - h // 2
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Apply Non-Maximum Suppression (NMS) to eliminate redundant boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)  # Lower NMS threshold
    print(f'Number of detections: {len(indexes)}')  # Debugging: Check number of detections
    
    # Draw the bounding boxes and labels
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])  # Use class name instead of class ID
            print(f'Detected: {label} with confidence: {confidences[i]}')  # Debugging: Print label and confidence
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            detected_labels.append(label)  # Store detected labels
    
    # Draw the rectangle at the bottom with the "Done" text (button-like)
    cv2.rectangle(frame, (0, height - 50), (width, height), (75, 0, 130), -1)  
    cv2.putText(frame, "Done", (width // 2 - 30, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # White text

    # Show the output image
    cv2.imshow("Detection", frame)

    # Stop detection if the user clicked on the "Done" button-like area
    if stop_detection:
       # open_vol_window(detected_labels)  # Open the window displaying the detected labels
        #cv2.destroyAllWindows()
        break
    
    # Press 'q' to exit (in case user doesn't click the button)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if stop_detection:
    open_vol_window(detected_labels) 







