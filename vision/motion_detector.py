import cv2
import numpy as np
import requests
from datetime import datetime, timezone
import time
import os
import subprocess

API_URL = "http://localhost:8000/events/"


def save_motion(event_type, image_url, video_url):
    payload = {
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "image_url": image_url,
        "video_url": video_url
    }

    try:
        response = requests.post(API_URL, json=payload)
        print(f"--- POST STATUS: {response.status_code} --- \n")

        if response.status_code == 200:
            print("--- Video sent to backend ---\n")

    except Exception as e:
        print("Failed to send POST:", e)


def convert_motion(input_path, output_path):
    if os.path.exists(input_path) and os.path.getsize(input_path) > 1000:
        command = [
            'ffmpeg',
            '-analyzeduration', '10000000',
            '-probesize', '10000000',
            '-i', input_path,
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        try:
            subprocess.run(command, check=True)
            print(f"--- Converted {input_path} to {output_path} ---\n")
        except subprocess.CalledProcessError as e:
            print(f"Conversion failed for {input_path}:", e)
    else:
        print(
            f"File size: {os.path.getsize(input_path)} bytes. \n VI file too small or does not exist.")


def detect_motion():
    video_path = ""
    previous_frame = None
    motion_writer = None
    motion_timer = 0
    motion_frames = 0
    motion_hold_frames = 30

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    print("***** Motion detection started *****")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if previous_frame is None:
            print(f"--- no movement detected ---\n")
            previous_frame = gray
            continue

        frame_diff = cv2.absdiff(previous_frame, gray)
        thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = any(cv2.contourArea(c) > 1000 for c in contours)

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if motion_detected:
            motion_timer = motion_hold_frames
            print(f"\nMOTION DETECTED!!!\n")
            # os.system("afplay assets/bark.wav")

        if motion_timer > 0:

            if motion_writer is None:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                video_dir = "static/videos"
                image_dir = "static/images"
                os.makedirs(video_dir, exist_ok=True)
                os.makedirs(image_dir, exist_ok=True)
                video_path = os.path.join(video_dir, f"motion_{timestamp}.avi")
                image_path = os.path.join(image_dir, f"image_{timestamp}.jpg")
                print("--- image and video created ---")
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                frame_resized = cv2.resize(frame, (640, 480))
                motion_writer = cv2.VideoWriter(
                    video_path, fourcc, 20.0, (640, 480))
                cv2.imwrite(image_path, frame)
                motion_frames = 0
                print(f"--- Recording motion to {video_path} ----")

            frame_resized = cv2.resize(frame, (640, 480))
            motion_writer.write(frame_resized)

            motion_frames += 1
            motion_timer -= 1

            if motion_frames >= 20 and motion_timer == 0:
                motion_writer.release()
                time.sleep(3)

                avi_path = video_path
                mp4_path = avi_path.replace(".avi", ".mp4")
                convert_motion(avi_path, mp4_path)

                if os.path.exists(mp4_path):
                    os.remove(avi_path)

                save_motion(
                    event_type="motion",
                    image_url=f"http://localhost:8000/{image_path}",
                    video_url=f"http://localhost:8000/{mp4_path}"
                )

                motion_writer = None

        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        previous_frame = gray

    print("\n***** Motion Detection ended *****")
    cap.release()
    cv2.destroyAllWindows()


def play_motion():
    video_folder = os.path.join("static", "videos")

    # Get sorted list of .avi files (newest first)
    videos = sorted(
        [vid for vid in os.listdir(video_folder) if vid.endswith(".mp4")],
        key=lambda x: os.path.getctime(os.path.join(video_folder, x)),
        reverse=True
    )

    if not videos:
        print("No videos found.")
        return

    print("\nAvailable videos:")
    for i, video in enumerate(videos):
        print(f"#{i + 1}. {video}")

    try:
        choice = int(input("\nEnter the number of the video to play: ")) - 1
        if not (0 <= choice < len(videos)):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    selected_video = os.path.join(video_folder, videos[choice])
    print(f"video is now playing...")

    cap = cv2.VideoCapture(selected_video)

    if not cap.isOpened():
        print("Error opening video file.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(f"{videos[choice]} ended.")
            choice = input(
                "Type 'cam' for motion detection or 'vid' to play another video or exit: ").strip().lower()
            if choice == 'cam':
                detect_motion()
            elif choice == 'vid':
                play_motion()
            else:
                break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Video Playback", gray)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    choice = input(
        "Type 'cam' for motion detection or 'vid' to play a video: ").strip().lower()
    if choice == 'cam':
        detect_motion()
    elif choice == 'vid':
        play_motion()
    else:
        print("NOOOOOOO.")
