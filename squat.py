import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return round(angle, 2)

# Initialize camera
cap = cv2.VideoCapture(1)  # Use 0 for default webcam

# Counter variables
left_counter, right_counter = 0, 0
left_stage, right_stage = None, None

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        height, width, _ = frame.shape

        # Convert to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Convert back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Left Side Landmarks
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * width,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * height]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * width,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * height]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * width,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * height]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height]

            # Right Side Landmarks
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

            # Convert positions to integers
            left_knee_pos = (int(left_knee[0]), int(left_knee[1]))
            right_knee_pos = (int(right_knee[0]), int(right_knee[1]))
            left_hip_pos = (int(left_hip[0]), int(left_hip[1]))
            right_hip_pos = (int(right_hip[0]), int(right_hip[1]))

            # Display angles on the screen
            cv2.putText(image, f'{int(left_knee_angle)}', left_knee_pos,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'{int(right_knee_angle)}', right_knee_pos,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, f'{int(left_hip_angle)}', left_hip_pos,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'{int(right_hip_angle)}', right_hip_pos,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)

            # Squat detection logic
            if left_hip_angle < 90 and left_knee_angle < 90:
                left_stage = "Down"
            if left_hip_angle > 160 and left_stage == "Down":
                left_stage = "Up"
                left_counter += 1

            if right_hip_angle < 90 and right_knee_angle < 90:
                right_stage = "Down"
            if right_hip_angle > 160 and right_stage == "Down":
                right_stage = "Up"
                right_counter += 1

        # Draw landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 200), thickness=2, circle_radius=2))

        # Display squat counts and stages
        cv2.putText(image, f'Left Squats: {left_counter}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(image, f'Right Squats: {right_counter}', (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(image, f'Left Stage: {left_stage}', (300, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, f'Right Stage: {right_stage}', (300, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Squat Detector', image)

        # Exit when 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
