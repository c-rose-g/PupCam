import cv2
import requests
from datetime import timezone, datetime
import os

API_URL = "https://localhost:8000/events"

previous_frame = None


def detect_motion():
    global previous_frame
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("error: could not open cam")
        return

    print("Motion detection started: Press 'q' to quit. ")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        print(f"ret: {ret}, frame type: {type(frame)}")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if previous_frame is None:
            previous_frame = gray
            continue

        frame_delta = cv2.absdiff(previous_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if motion_detected:
            print("MOTION DETECTED!")

            try:
                requests.post("http://localhost:8000/events", json={
                    "event": "motion_detected",
                })
                os.system("afplay assets/bark.wav")
            except Exception as e:
                print(f"Error posting to backend: {e}")

        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def send_motion_event_to_backend():
    payload = {"event_type": "motion",
               "image_url": "https://example.com/image.jpg",
               "video_url": "https://example.com/video.mp4",
               "user_id": "dev-test",
               }
    try:
        response = requests.post(API_URL, json=payload)
        print("POST STATUS:", response.status_code)
    except Exception as e:
        print("Failed to send POST:", e)


if __name__ == "__main__":
    detect_motion()
