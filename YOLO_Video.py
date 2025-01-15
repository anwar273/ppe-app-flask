import cv2
import torch
import torchvision
import math
from ultralytics import YOLO
import pygame  # Import pygame for playing sound

def video_detection(path_x):
    # Initialize pygame mixer for sound
    pygame.mixer.init()
    alert_sound = pygame.mixer.Sound('emergency-siren-alert-single-epic-stock-media-1-00-01.mp3')  # Replace with the path to your sound file

    # Check if CUDA is available and use GPU if possible
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Log the device being used
    print(f"Using device: {device}")

    cap = cv2.VideoCapture(path_x)

    if not cap.isOpened():
        raise ValueError(f"Error opening video file: {path_x}")

    # Load the YOLO model
    model = YOLO('best8.pt')

    # Class names and colors for each class
    classNames = {0: 'Hardhat', 1: 'Mask', 2: 'NO-Hardhat', 3: 'NO-Mask', 4: 'NO-Safety Vest',
                  5: 'Person', 6: 'Safety Cone', 7: 'Safety Vest', 8: 'machinery', 9: 'vehicle'}

    colors = {
        'Hardhat': (255, 0, 0),  # Red
        'Mask': (0, 255, 0),  # Green
        'NO-Hardhat': (0, 0, 255),  # Blue
        'NO-Mask': (255, 255, 0),  # Cyan
        'NO-Safety Vest': (0, 255, 255),  # Yellow
        'Person': (255, 0, 255),  # Magenta
        'Safety Cone': (255, 255, 255),  # White
        'Safety Vest': (128, 128, 128),  # Gray
        'machinery': (128, 0, 128),  # Purple
        'vehicle': (0, 128, 128)  # Teal
    }

    try:
        while True:
            success, img = cap.read()
            if not success:
                break

            # Resize image for faster processing
            img_resized = cv2.resize(img, (640, 480))

            # Convert BGR to RGB for the model
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

            # Normalize and prepare image for the model
            img_rgb = img_rgb.astype('float32') / 255.0
            img_tensor = torch.tensor(img_rgb).permute(2, 0, 1).unsqueeze(0).float().to(device)

            # Perform inference
            results = model(img_tensor)

            # Flag to check if PPE-related objects are detected
            ppe_detected = False

            # Process the detections
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls_index = int(box.cls)

                    if cls_index in classNames:
                        class_name = classNames[cls_index]
                        if class_name in ['Hardhat', 'Mask', 'Safety Vest']:
                            ppe_detected = True

                        label = f'{class_name} {conf:.2f}'
                        color = colors[class_name]

                        # Draw bounding box and label
                        cv2.rectangle(img_resized, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(img_resized, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Play sound if no PPE is detected
            if not ppe_detected:
                pygame.mixer.Sound.play(alert_sound)

            # Yield the processed frame with detections
            yield img_resized

    finally:
        cap.release()
        pygame.mixer.quit()
