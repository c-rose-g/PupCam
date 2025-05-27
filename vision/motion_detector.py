import cv2
import requests
from datetime import timezone, datetime
import time
import json

API_URL = "http://localhost:8000/events/"

MIN_AREA = 5000  # Adjust for motion sensitivity
COOLDOWN_SECONDS = 5
previous_frame = None
last_motion_time = 0  # Global cooldown timer

def send_motion_event_to_backend(event_type, image_url, video_url):
    payload = {
        "event_type": event_type,
        "image_url": image_url,
        "video_url": video_url,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    try:
        print("PAYLOAD SENT:", json.dumps(payload, indent=2))
        response = requests.post(API_URL, json=payload)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
    except Exception as e:
        print("Failed to send POST:", e)


def detect_motion():
    global previous_frame, last_motion_time

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    print("Motion detection started. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if previous_frame is None:
            previous_frame = gray
            continue

        frame_delta = cv2.absdiff(previous_frame, gray)
        thresh = cv2.threshold(frame_delta, 50, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        total_motion_area = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < MIN_AREA:
                continue
            motion_detected = True
            total_motion_area += area
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Post only if motion detected, over threshold, and cooldown expired
        current_time = time.time()
        if motion_detected and total_motion_area > MIN_AREA and (current_time - last_motion_time > COOLDOWN_SECONDS):
            send_motion_event_to_backend(
                "motion",
                "https://example.com/image.jpg",
                "https://example.com/video.mp4"
            )
            last_motion_time = current_time

        previous_frame = gray
        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            print("Quitting motion detection")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_motion()
