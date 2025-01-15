import os

import cv2
from flask import Flask, render_template, Response, session
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

from YOLO_Video import video_detection

app = Flask(__name__)

app.config['SECRET_KEY'] = '0000'
app.config['UPLOAD_FOLDER'] = 'static/Videos'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Run")


def generate_frames(path_x=''):
    yolo_output = video_detection(path_x)
    frame_counter = 0
    skip_frames = 5  # Only process every 5th frame

    for detection_ in yolo_output:
        # Skip frames to process every nth frame
        if frame_counter % skip_frames != 0:
            frame_counter += 1
            continue

        # Encode frame to JPEG with reduced quality
        ret, buffer = cv2.imencode('.jpg', detection_, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')
        frame_counter += 1


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    session.clear()
    return render_template('index-project.html')


@app.route('/webcam')
def webcam():
    session.clear()
    return render_template('ui.html')


@app.route('/FrontPage', methods=['GET', 'POST'])
def front():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('video-poject.html', form=form)


@app.route('/video')
def video():
    return Response(generate_frames(path_x=session.get('video_path', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webapp')
def webapp():
    return Response(generate_frames(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_test')
def video_static():
    return Response(generate_frames(path_x=r"Videos\4.mp4"), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)

