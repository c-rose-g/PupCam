import cv2
import numpy as np
import requests
from datetime import timezone, datetime
import time
import os
import subprocess

API_URL = "http://localhost:8000/events/"
MIN_AREA = 500
COOLDOWN_SECONDS = 3
previous_frame = None
last_motion_time = 0
motion_writer = None
motion_frames = 0
MOTION_CLIP_LENGTH = 60


def convert_avi_to_mp4(source_path, target_path):
    try:
        subprocess.run(
            ["ffmpeg", "-i", source_path, "-vcodec", "libx264", "-crf", "23", target_path],
            check=True
        )
        print(f"Converted {source_path} to {target_path}")
    except subprocess.CalledProcessError:
        print(f"Failed to convert {source_path}")


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

    if not cap.isOpened():
        print("error: could not open cam")
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create a new video file
        filename = f"motion_{int(timestamp)}.avi"
        # create a snapshot image
        image_filename = f"frame_{timestamp}.jpg"
        # if motion is detected, and there is motion happening (like if a person walks across the camera), save that video
        if motion_detected and total_motion_area > MIN_AREA and (current_time - last_motion_time > COOLDOWN_SECONDS):
            print("\nMOTION DETECTED!!!")
            os.system("afplay assets/bark.wav")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')

            video_path = os.path.join("static", "videos", filename)
            image_path = os.path.join("static", "images", image_filename)

            motion_writer = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
            cv2.imwrite(image_path, frame)
            motion_frames = 0
            last_motion_time = current_time

            send_motion_event_to_backend(
                "motion",
                f"http://localhost:8000/static/images/{image_filename}",
                f"http://localhost:8000/static/videos/{filename}"
            )

        # If currently recording a motion event, write the frame
        if motion_writer is not None:
            print(f"- Recording motion frame: {motion_frames} to {video_path}")
            motion_writer.write(frame)
            motion_frames += 1

            # Stop after saving enough frames
            # if motion_frames >= MOTION_CLIP_LENGTH:
            #     print("* Recording saved * \n")
            #     motion_writer.release()
            #     motion_writer = None
            #     mp4_path = os.path.join("static", "videos", filename.replace(".avi", ".mp4"))
            #     convert_avi_to_mp4(video_path, mp4_path)
            if motion_writer is not None and motion_frames > 0:
                print("* Recording saved * \n")
                motion_writer.release()
                motion_writer = None

                if os.path.getsize(video_path) > 0:
                    mp4_path = video_path.replace(".avi", ".mp4")

            convert_avi_to_mp4(video_path, mp4_path)

        frame = cv2.flip(frame, 0)

        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        previous_frame = gray

    print("\n***** Motion Detection ended *****")
    cap.release()
    cv2.destroyAllWindows()

def play_video_from_db():
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
    print(f"\nPlaying: {selected_video}")

    cap = cv2.VideoCapture(selected_video)

    if not cap.isOpened():
        print("Error opening video file.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("error or video is over.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Video Playback", gray)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    choice = input("Type '1' for motion detection or return to play a video: ").strip().lower()
    if choice == '1':
        detect_motion()
    elif choice == chr(' '):
        play_video_from_db()
    else:
        print("NOOOOOOO.")
