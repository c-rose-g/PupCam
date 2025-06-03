import cv2
import numpy as np
import requests
from datetime import timezone, datetime
import time
import os

API_URL = "http://localhost:8000/events/"
MIN_AREA = 500
COOLDOWN_SECONDS = 1
previous_frame = None
last_motion_time = 0
motion_writer = None
motion_frames = 0
MOTION_CLIP_LENGTH = 60

def send_motion_event_to_backend(event_type, image_url, video_url):

    payload = {"event_type": event_type,
               "image_url": image_url,
               "video_url": video_url,
               "timestamp": datetime.now(timezone.utc).isoformat()
               }
    try:
        response = requests.post(API_URL, json=payload)
        print("POST STATUS:", response.status_code)
    except Exception as e:
        print("Failed to send POST:", e)


def detect_motion():
    global previous_frame, last_motion_time, motion_writer, motion_frames

    cap = cv2.VideoCapture(0)
    # define the codec (still don't get what this is) and create VideoWriter obj
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    if not cap.isOpened():
        print("error: could not open cam")
        exit()

    print("Motion detection started")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # operations on the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
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
        # if motion is detected, and there is motion happening (like if a person walks across the camera), save that video
        if motion_detected and total_motion_area > MIN_AREA and (current_time - last_motion_time > COOLDOWN_SECONDS):
            print("Motion detected, saving video clip...")
            # Create a new video file for this motion event
            filename = f"motion_{int(current_time)}.avi"
            motion_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            motion_frames = 0
            # send_motion_event_to_backend(
            #     "motion",
            #     "https://example.com/image.jpg",
            #     "https://example.com/video.mp4"
            # )
            last_motion_time = current_time

        # If currently recording a motion event, write the frame
        if motion_writer is not None:
            motion_writer.write(frame)
            motion_frames += 1
            # Stop after saving enough frames
            if motion_frames >= MOTION_CLIP_LENGTH:
                motion_writer.release()
                motion_writer = None

        previous_frame = gray
        frame = cv2.flip(frame, 0)
        # write the flipped frame
        out.write(frame)

        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        previous_frame = gray

    cap.release()
    cap.release()
    cv2.destroyAllWindows()

def play_video_from_db():
    cap = cv2.VideoCapture('vtest.avi')

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("can't recieve frame (stream end). exiting")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    return

if __name__ == "__main__":
    detect_motion()
