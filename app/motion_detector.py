from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import com
import config
import traceback
import _thread



def compare():
    try:
        url = config.stream

        min_area = config.min_area
        max_area = config.max_area
        
        counter = 0
        threashold = config.threashold
        delay = config.delay
        framerate = config.framerate
        
        # initialize the first frame in the video stream
        vs = cv2.VideoCapture(url)
        firstFrame = None
        # loop over the frames of the video
        while True:

            frame = vs.read()[1]
            text = "Unoccupied"

            # if the frame could not be grabbed, then we have reached the end of the video
            if frame is None:
                retry("frame was none")

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (31, 31), 0)

            cv2.imshow("frame", frame)
            cv2.imshow("gray", gray)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            frameDelta = cv2.absdiff(gray, firstFrame)
            thresh = cv2.threshold(frameDelta, threashold, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # loop over the contours
            for c in cnts:
                if cv2.contourArea(c) < min_area or cv2.contourArea(c) > max_area:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"

            # draw the text and timestamp on the frame
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if text == "Occupied" and config.monitor:
                img = frame
                location = com.saveImage(img)
                _thread.start_new_thread(com.notify, (location, ) )

            # get new image to compare to every so often to avoid changes over time ie. sun
            counter+=1
            if counter % (framerate * delay) == 0:
                firstFrame = gray

    except Exception as e: 
        traceback.print_exc()
        retry(e)
        
        
def retry(error):
    print(error)
    time.sleep(10)
    compare()
