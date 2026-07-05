import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
from streamlit_webrtc import VideoProcessorBase
import cv2
import av

CLOSED_CONSECUTIVE_FRAMES = 30
YAWN_CONSECUTIVE_FRAMES = 5
CONFIDENCE_THRESHOLD = 0.5


class DrowsinessVideoProcessor(VideoProcessorBase):
    def __init__(self, model):
        self.model = model 
        self.sleep_counter = 0
        self.yawn_counter = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        DEVICE = 0 if torch.cuda.is_available() else "cpu"
        results = self.model.predict(img, device=DEVICE, imgsz=320, conf=0.35, verbose=False)
        
        eye_closed = False
        yawning = False
     
        for result in results:
            for box in result.boxes:
                confidence = float(box.conf[0])
                if confidence < CONFIDENCE_THRESHOLD:
                    continue
                cls = int(box.cls[0])
                label = self.model.names[cls].lower()
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"{label} {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                if label == "close" and confidence >= 0.5:
                    eye_closed = True

                elif label == "yawn" and confidence >= 0.08:
                    yawning = True

        if eye_closed:
            self.sleep_counter += 1
        else:
            self.sleep_counter = 0

        if self.sleep_counter >= CLOSED_CONSECUTIVE_FRAMES:
            cv2.putText(img, "DROWSINESS DETECTED!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
        if yawning:
            self.yawn_counter += 1
        else:
            self.yawn_counter = 0

        if self.yawn_counter >= YAWN_CONSECUTIVE_FRAMES:
            cv2.putText(img, "YAWNING WARNING!", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
    
        cv2.putText(img, f"Closed Frames: {self.sleep_counter}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, f"Yawn Frames: {self.yawn_counter}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")