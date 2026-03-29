# Importing necessary libraries
from flask import Flask, render_template, Response, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
import subprocess


# Initialize Flask app
app = Flask(__name__) 

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


left_counter, right_counter = 0, 0 # Counters for bicep curls
left_stage, right_stage = None, None # Stages for bicep curls
counter_enabled = False   # Boolean to enable/disable counting
squat_counter =0 # Counter for squats
squat_stage = None # Stage for squats
pushup_counter =0
pushup_stage = None
crunches_counter =0
crunches_stage =None
# Function to calculate angle between three points (used for joint angles)
def calculate_angle(a, b, c):
    a = np.array(a) # Convert to NumPy arrays
    b = np.array(b)
    c = np.array(c)

    # Compute angle using arctan2 function
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    # Ensure the angle is within 0-180 degrees
    if angle > 180.0:
        angle = 360 - angle

    return round(angle, 2) # Return rounded angle

# Function to process frames for bicep curls tracking

def curls_frames():
    global left_counter, right_counter, left_stage, right_stage, counter_enabled

    cap = cv2.VideoCapture(0)   # Open webcam (1 for external, 0 for internal)

     # Initialize MediaPipe Pose detection
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()  # Read frame from webcam
            if not ret:  # Break loop if frame not available
                break

            height, width, _ = frame.shape  # Get frame dimensions
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert to RGB
            image.flags.writeable = False  # Improve performance
            results = pose.process(image)   # Process frame with MediaPipe Pose

            image.flags.writeable = True   # Re-enable modifications
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV

            # If landmarks detected, process them
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                # Extract key joint positions for left and right sides
                # Left Side
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * width,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * height]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * width,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * height]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * width,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * height]

                # Right Side
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * width,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * height]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * width,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * height]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * width,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * height]

                # Calculate angles for bicep curls
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)

                # Display angles on screen
                cv2.putText(image, f"{int(left_elbow_angle)}", (int(left_elbow[0]), int(left_elbow[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f"{int(right_elbow_angle)}", (int(right_elbow[0]), int(right_elbow[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f"{int(left_shoulder_angle)}", (int(left_shoulder[0]), int(left_shoulder[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, f"{int(right_shoulder_angle)}", (int(right_shoulder[0]), int(right_shoulder[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

                # Bicep curl counter logic
                if counter_enabled:
                    if 15 <= left_shoulder_angle <= 25:
                        if left_elbow_angle > 140:
                            left_stage = "Down"
                        if left_elbow_angle < 35 and left_stage == 'Down':
                            left_stage = "Up"
                            left_counter += 1

                    if 15 <= right_shoulder_angle <= 25:
                        if right_elbow_angle > 150:
                            right_stage = "Down"
                        if right_elbow_angle < 35 and right_stage == 'Down':
                            right_stage = "Up"
                            right_counter += 1
                # Draw landmarks
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            # Encode processed frame for streaming
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()   # Release webcam
    cv2.destroyAllWindows()  # Close OpenCV windows

#Function to process frames for Squat tracking
def squat_frames():
    global squat_counter, squat_stage, counter_enabled

    cap = cv2.VideoCapture(0)  

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

                # Left Side
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * width,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * height]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * width,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * height]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * width,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * height]
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height]

                # Right Side
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * width,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * height]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * width,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * height]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * width,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * height]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]

                # Calculate angles
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)

                # Display angles on screen
                cv2.putText(image, f"{int(left_knee_angle)}", (int(left_knee[0]), int(left_knee[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f"{int(right_knee_angle)}", (int(right_knee[0]), int(right_knee[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f"{int(left_hip_angle)}", (int(left_hip[0]), int(left_hip[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f"{int(right_hip_angle)}", (int(right_hip[0]), int(right_hip[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

                # Squat counter logic
                if counter_enabled:
                    if left_hip_angle <= 100 and left_knee_angle < 90:
                        squat_stage = "Down"
                    if left_hip_angle > 150 and squat_stage == "Down":
                        squat_stage = "Up"
                        squat_counter += 1
                    if right_hip_angle <= 100 and right_knee_angle < 90:
                        squat_stage = "Down"
                    if right_hip_angle > 150 and squat_stage == "Down":
                        squat_stage = "Up"
                        squat_counter += 1

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

#Function to process frames for Push tracking
def Pushup_frames():
    global pushup_counter, pushup_stage, counter_enabled

    cap = cv2.VideoCapture(0)  

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

                # Left Side
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * width,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * height]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * width,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * height]

                # Right Side
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * width,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * height]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * width,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * height]

                # Calculate angles
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Display angles on screen
                cv2.putText(image, f"{int(left_elbow_angle)}", (int(left_elbow[0]), int(left_elbow[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f"{int(right_elbow_angle)}", (int(right_elbow[0]), int(right_elbow[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

                # Pushup counter logic
                if counter_enabled:
                    if left_elbow_angle < 90 and right_elbow_angle < 90:
                        pushup_stage = "Down"
                    if left_elbow_angle > 160 and right_elbow_angle > 160 and pushup_stage == "Down":
                        pushup_stage = "Up"
                        pushup_counter += 1

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

def Crunches_frames():
    global crunches_counter, crunches_stage, counter_enabled

    cap = cv2.VideoCapture(0)  

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

                # Left 
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * width,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * height]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * width,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * height]
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height]

                #Right
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * width,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * height]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * width,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * height]

                # Calculate angles
                left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)

                # Display angles on screen
                cv2.putText(image, f"L: {int(left_hip_angle)}", (int(left_hip[0]), int(left_hip[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, f"R: {int(right_hip_angle)}", (int(right_hip[0]), int(right_hip[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)


                # Pushup counter logic
                if counter_enabled:
                    if left_hip_angle < 100 and right_hip_angle < 100:
                        crunch_stage = "Up"
                    if left_hip_angle > 130 and right_hip_angle > 130 and crunch_stage == "Up":
                        crunch_stage = "Down"
                        crunches_counter += 1


                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            #For live video stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()


# Flask Routes
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

@app.route('/start-pushup')
def start_pushup():
    return render_template('Pushup.html')

@app.route('/start-crunches')
def start_crunches():
    return render_template('crunches.html')



@app.route('/bicep_curl_feed')
def bicep_curl_feed():
    return Response(curls_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/squat_feed')
def squat_feed():
    return Response(squat_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/Pushup_feed')
def Pushup_feed():
    return Response(Pushup_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/crunches_feed')
def crunches_feed():
    return Response(Crunches_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_counts')
def get_counts():
    return jsonify({'left_counter': left_counter, 'right_counter': right_counter, 'left_stage': left_stage, 'right_stage': right_stage})

@app.route('/get_squat_counts')
def get_squat_counts():
    return jsonify({'squat_counter': squat_counter, 'squat_stage': squat_stage})

@app.route('/get_Pushup_counts')
def get_Pushup_counts():
    return jsonify({'pushup_counter': pushup_counter, 'pushup_stage': pushup_stage})

@app.route('/get_crunches_counts')
def get_crunches_counts():
    return jsonify({'crunches_counter': crunches_counter, 'crunches_stage': crunches_stage})

@app.route('/toggle_counter', methods=['POST'])
def toggle_counter():
    global counter_enabled
    counter_enabled = not counter_enabled  
    return jsonify({'counter_enabled': counter_enabled})


#run flask applications
if __name__ == "__main__":
    app.run(debug=True)
