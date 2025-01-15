# Web Application: YOLO Object Detection

## Overview
This web application implements object detection using the YOLOv8 model. It provides functionalities for video analysis, live webcam detection, and file uploads for object detection tasks. The application uses Flask for its backend and incorporates Bootstrap for a responsive and user-friendly interface.

---

## Features

1. **Video Analysis**:
   - Upload videos for object detection.
   - Visualize the detection results with bounding boxes and labels.

2. **Live Webcam Detection**:
   - Real-time object detection via webcam.

3. **User-Friendly Interface**:
   - Responsive design using Bootstrap.
   - Navigation menu for easy access to features.

---

## Installation

### Prerequisites
Ensure the following are installed on your system:
- Python 3.7 or later
- pip (Python package installer)
- Virtual environment tools (optional but recommended)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/anwar273/ppe-app-flask
   cd ppe-app-flask
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the YOLO Model**:
   - Download the YOLOv11 model weights (`best1.pt`) and place it in the project directory.

5. **Run the Application**:
   ```bash
   python flaskApp.py
   ```
   The application will be available at `http://127.0.0.1:5000`.

---

## File Structure

```
├── flaskApp.py           # Main Flask application file
├── YOLO_Video.py         # YOLO video processing logic
├── templates/            # HTML templates
│   ├── index-project.html
│   ├── video-poject.html
│   └── ui.html
├── static/
│   ├── Videos/          # Uploaded videos
│   └── images/          # Static images for the application
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Usage

1. **Home Page**:
   - Navigate to the home page (`/home`) for an overview.

2. **Upload a Video**:
   - Go to `/FrontPage` to upload a video for object detection.

3. **Live Webcam Detection**:
   - Visit `/webcam` to access the live webcam detection feature.

4. **View Results**:
   - Processed frames with detection results will be displayed in real-time.

---

## Technologies Used

- **Backend**:
  - Python
  - Flask

- **Frontend**:
  - HTML/CSS
  - Bootstrap

- **Object Detection**:
  - YOLOv8
  - PyTorch

---

## Future Enhancements

1. Integrate more advanced YOLO versions for better detection.
2. Add support for multiple video uploads.
3. Improve the UI/UX with animations and interactive graphs.
4. Enhance error handling and feedback for better usability.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributors
- **Your Name**: [Your GitHub](https://github.com/your-profile)

---

## Support
For any issues, please open a GitHub issue or contact [your-email@example.com].

