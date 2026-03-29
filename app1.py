from flask import Flask, render_template, Response, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3

app = Flask(__name__)

#Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate',150)


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

left_counter, right_counter = 0, 0
left_stage, right_stage = None, None
squat_counter = 0
squat_stage = None
counter_enabled = False  

def speak(text):
    #Function to convert text to speech
    engine.say(text)
    engine.runAndWait()

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return round(angle, 2)

def curls_frames():
    global left_counter, right_counter, left_stage, right_stage, counter_enabled

    cap = cv2.VideoCapture(1)  

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            height, width, _ = frame.shape
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * width,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * height]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * width,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * height]

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * width,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * height]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * width,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * height]

                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                cv2.putText(image, f"{int(left_elbow_angle)}", (int(left_elbow[0]), int(left_elbow[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f"{int(right_elbow_angle)}", (int(right_elbow[0]), int(right_elbow[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

                if counter_enabled:
                    if left_elbow_angle > 140:
                        left_stage = "Down"
                        speak(left_stage)
                    if left_elbow_angle < 35 and left_stage == 'Down':
                        left_stage = "Up"
                        left_counter += 1
                        

                    if right_elbow_angle > 150:
                        right_stage = "Down"
                    if right_elbow_angle < 35 and right_stage == 'Down':
                        right_stage = "Up"
                        right_counter += 1

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

def squat_frames():
    global squat_counter, squat_stage, counter_enabled

    cap = cv2.VideoCapture(1)  

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            height, width, _ = frame.shape
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * width,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * height]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * width,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * height]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * width,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * height]

                knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                
                cv2.putText(image, f"{int(knee_angle)}", (int(left_knee[0]), int(left_knee[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

                if counter_enabled:
                    if knee_angle > 160:
                        squat_stage = "Up"
                    if knee_angle < 90 and squat_stage == 'Up':
                        squat_stage = "Down"
                        squat_counter += 1

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/squat_feed')
def squat_feed():
    return Response(squat_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def ai_trainer():
    return render_template('Fitproconnect.html')

@app.route('/Service-ai')
def Service_ai():
    return render_template('Service-ai.html')

@app.route('/start-bicep_curl')
def start_workout():
    return render_template('bicep_curl.html')

@app.route('/start-squat')
def start_squat():
    return render_template('squat.html')

@app.route('/bicep_curl_feed')
def bicep_curl_feed():
    return Response(curls_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/get_counts')
# def get_counts():
#     return jsonify({'left_counter': left_counter, 'right_counter': right_counter, 'left_stage': left_stage, 'right_stage': right_stage})
@app.route('/get_counts')
def get_counts():
    return jsonify({'left_counter': left_counter, 'right_counter': right_counter, 'squat_counter': squat_counter})


@app.route('/toggle_counter', methods=['POST'])
def toggle_counter():
    global counter_enabled
    counter_enabled = not counter_enabled  
    return jsonify({'counter_enabled': counter_enabled})

if __name__ == "__main__":
    app.run(debug=True)