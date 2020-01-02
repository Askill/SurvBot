# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import com
import config

def compare():
    try:
        url = config.stream
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-amin", "--min-area", type=int, default=3000, help="minimum area size")
        ap.add_argument("-amax", "--max-area", type=int, default=10000, help="minimum area size")
        args = vars(ap.parse_args())

        # if the video argument is None, then we are reading from webcam
        args["video"] = url
        #args["video"] = "./videos/example_02.mp4"
        vs = cv2.VideoCapture(args["video"])
        counter = 0
        threashold = 18
        delay = .3
        framerate = 30

        # initialize the first frame in the video stream
        firstFrame = None

        # loop over the frames of the video
        while True:
           
            # grab the current frame and initialize the occupied/unoccupied
            # text
            frame = vs.read()
            frame = frame if args.get("video", None) is None else frame[1]
            text = "Unoccupied"

            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if frame is None:
                retry("frame was none")

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            #frame = increase_brightness(frame, value=50)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (31, 31), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(gray, firstFrame)

            thresh = cv2.threshold(frameDelta, threashold, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < args["min_area"]:
                    continue
                if cv2.contourArea(c) > args["max_area"]:
                    continue
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text

                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"

            # draw the text and timestamp on the frame
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if text == "Occupied" and config.monitor:
                img = frame
                location = com.saveImage(img)
                com.notify(location)
                print(text)

            counter+=1
            if counter % (framerate * delay) == 0:
                firstFrame = gray

    except Exception as e: 
        retry(e)
        # cleanup the camera and close any open windows
        vs.stop() if args.get("video", None) is None else vs.release()
        
def retry(error):
    print(error)
    time.sleep(10)
    compare()
