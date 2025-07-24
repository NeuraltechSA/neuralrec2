from __future__ import annotations
import cv2
import time
from typing import List
import numpy as np
from cv2.typing import MatLike

# 700,600 1250,590 2550 990 2557 1434 1740 1426

class MotionDetector:
    __last_frame: MatLike | None = None
    __min_contour_area: int = 100
    __count = 0
    
    def __init__(self, motion_area: List[tuple[float, float]]):
        self.__motion_area = motion_area
    
    def crop_motion_area(self, frame:MatLike):
        # Cropping polygon
        motion_area_px = [(int(x*frame.shape[1]), int(y*frame.shape[0])) for x,y in self.__motion_area]
        points = np.array(motion_area_px)
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [points], 255)
        return cv2.bitwise_and(frame, frame, mask=mask)
    
    def get_contour_detections(self, mask:MatLike, thresh:int=400):
        """ Obtains initial proposed detections from contours discoverd on the mask. 
        Scores are taken as the bbox area, larger is higher.
        Inputs:
            mask - thresholded image mask
            thresh - threshold for contour size
        Outputs:
            detectons - array of proposed detection bounding boxes and scores [[x1,y1,x2,y2,s]]
        """
        # get mask contours
        contours, _ = cv2.findContours(mask, 
                                    cv2.RETR_EXTERNAL, # cv2.RETR_TREE, 
                                    cv2.CHAIN_APPROX_TC89_L1)
        detections = []
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            area = w*h
            if area > thresh: 
                detections.append([x,y,x+w,y+h, area])

        return np.array(detections)
    
    def detect_motion(self, frame:MatLike):
        self.__count += 1
        if self.__last_frame is None or self.__count < 2:
            self.__last_frame = frame
            return
        self.__count = 0
        
        gray_current = cv2.cvtColor(self.crop_motion_area(frame), cv2.COLOR_BGR2GRAY)
        gray_last = cv2.cvtColor(self.crop_motion_area(self.__last_frame), cv2.COLOR_BGR2GRAY)
        
        result = np.abs(np.mean(gray_current) - np.mean(gray_last))

        frame_diff = cv2.absdiff(gray_current, gray_last)
        motion_area =self.crop_motion_area(frame)
        thresholded_motion_area = cv2.threshold(frame_diff, 90, 255, cv2.THRESH_BINARY)[1]
        thresholded_motion_area = cv2.morphologyEx(thresholded_motion_area, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
        
        detections = self.get_contour_detections(thresholded_motion_area)
        for detection in detections:
            cv2.rectangle(motion_area, (detection[0], detection[1]), (detection[2], detection[3]), (0, 255, 0), 2)
        
        
        
        #cv2.imshow("frame_cnt", frame_cnt)
        #contours, _ = cv2.findContours(frame_diff, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #frame_cnt = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
        #cv2.imshow("frame_cnt", frame_cnt)
        #print(result)
        #if result > 0.3:
        #    print("MOTION")
        #    cv2.imshow("frame_diff", frame_diff)
        #cv2.imshow("frame", frame)
        
        #cv2.imshow("thresholded_motion_area", thresholded_motion_area)
        #cv2.imshow("frame_diff", frame_diff)
        #cv2.imshow('motion_area', motion_area)
        
        #cv2.waitKey(1)
        self.__last_frame = frame
        #print(frame_diff)
        
    
    
    '''
    def find_moving_objects(self, frame:MatLike, fgbg:cv2.BackgroundSubtractorMOG2):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(opening, kernel)
        _, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(bins, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return hierarchy, contours

    
    def detect_motion(self, frame:MatLike):
        background_subtractor = cv2.createBackgroundSubtractorMOG2()
        hierarchy, contours = self.find_moving_objects(frame, background_subtractor)
    '''


# Convertir coordenadas de píxeles a porcentajes (0-1) para resolución 2560x1440
# Original: [(700, 600), (1250, 590), (2550, 990), (2557, 1434), (1740, 1426)]
motion_area = [
    (0.273, 0.417),
    (0.488, 0.410),
    (0.996, 0.688),
    (0.999, 0.996),
    (0.680, 0.990)
]


#motion_area = [(700, 600), (1250, 590), (2550, 990), (2557, 1434), (1740, 1426)]
#motion_area = [(2045, 292),(2399,320),(691,1423),(0,1429),(0, 805)]

motion_detector = MotionDetector(motion_area)

# video_path = "file:///app/Saladas (descendente)_2025-07-20_09-30-10.mkv"
video_path = "file:///app/San Lorenzo (descendente)_2025-07-14_14-01-05.mkv"
#video_path = "file:///app/San Lorenzo (ascendente)_2025-07-19_13-00-31.mkv"
cap = cv2.VideoCapture(video_path)
start_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (320, 180))
    motion_detector.detect_motion(frame)
cap.release()
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")