# encoding=utf-8

import cv2
import numpy as np
import base64
import requests
videoname = "R2024-05-14_20-16-13_BJ21_p2.mp4"

cap = cv2.VideoCapture(videoname)
winname = 'detector tf2'
# Set the mouse callback for the window
cv2.namedWindow(winname)
nframe = 0
while True:
    ret, frame = cap.read()
    nframe += 1
    if not ret or frame is None:
        logger.info('Failed to read frame from video')
        continue

    # Exit condition
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q') or cv2.getWindowProperty(winname, cv2.WND_PROP_AUTOSIZE) < 1: 
        cv2.destroyAllWindows()
        break

    # cv2.waitKey(1)
    cv2.imshow(winname, frame)

    if(nframe == 500):
        # cv2.imwrite("testframe.jpg", frame)

        # Encode the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)

        # Convert the encoded frame to base64
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        img_base64N = len(frame_base64)  # Calculate the length of the base64 string

        # # Encode the base64 string for form data
        # encoded_base64 = urllib.parse.quote_plus(frame_base64)

        # Prepare the payload
        payload = {
            'msg': 'Frame from client',
            'imgbase64': frame_base64,
            'img_base64N': img_base64N,
            'img_w': frame.shape[1],
            'img_h': frame.shape[0],
            'img_N': frame.size
        }
        # Debugging: Print lengths and values
        print(f"Length of frame_base64: {len(frame_base64)}")
        print(f"Value of img_base64N: {img_base64N}")
        print(f"First 50 chars of frame_base64: {frame_base64[:50]}...")

        engine_predict_URL = "http://10.146.11.75:5000/countsPredict"

        response = requests.post(engine_predict_URL, data=payload)
        # Check response
        if response.status_code == 200:
            print("Frame sent successfully!")
            print(f"Response: {response.json()}")
            resp_json = response.json()
            # desc, score, predict_suits, predict_cardval, classid
            ith = 0 # ith card
            desc = resp_json['msg']
            score = resp_json['nScore'].split(",")[ith]
            classid = resp_json['nClass'].split(",")[ith]
            print(classid)

        else:
            print(f"Failed to send frame. Status code: {response.status_code}")
            print(f"Response: {response.text}")

        break

