from src.notifications import TwilioNotifier
from src.utils import Conf
from imutils.video import VideoStream
from datetime import datetime
from datetime import date
import imutils
import signal
import time
import cv2
import sys
import os

# Enter save path if you want to save captures locally.
savePath = "Enter directory to save files to."

# Generate file name.
def get_file_name():
    filename = datetime.now().strftime("%d %B %Y %I:%M:%S%p").replace(" ", "-") + ".mp4"
    filename = os.path.join(savePath, filename)
    res = filename.replace(":", '-')
    return res

# Handle keyboard interrupts.
def signal_handler(sig, frame):
    print("You pressed `CTRL + C`! Closing application...")
    sys.exit(0)

# Load configuration.
conf_path = "config.json"
conf = Conf(conf_path)
notif = TwilioNotifier(conf)

# Initialize indicators.
sent = False
motion = False
avg = None
startTime = datetime.now()

# Initialize dimensions and writer.
H = None
W = None
writer = None
cap = None

# Start video stream.
print("Starting camera...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(5)

# Signal trap to handle keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)
print("Press `CTRL + C` to exit the program.")

# Loop over frames from stream.
while True:
    # Get time and status.
    timestamp = datetime.now()
    status = "Unoccupied."
    prevMotion = motion

    # Grab frame and resize.
    frame = vs.read()

    # Convert frame to grayscale and blur.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Initialize average frame.
    if avg is None:
        print("Starting background model...")
        avg = gray.copy().astype("float")
        continue

    # Initialize dimensions based on frame.
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    # Compute diff between average frame and current frame.
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # Threshold the delta.
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Get contours of delta.
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Loop over contours.
    for c in contours:
        # Ignore small contours.
        if cv2.contourArea(c) < conf["min_area"]:
            continue

        # Draw bounding box.
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Update status.
        status = "Occupied"

    if status == "Occupied":
        motion = True

    # Add status and timestamp to output frame.
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Room Status: {}".format(status), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # Check if motion has just been detected.
    if motion and not prevMotion:
        startTime = datetime.now()

        # Initialize the video writer object at specified file path.
        cap = get_file_name()
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        writer = cv2.VideoWriter(cap, fourcc, 30, (W, H), True)

    # Check if length of output video fulfills requirements.
    elif prevMotion:

        # Get time difference.
        timeDelta = (datetime.now() - startTime).seconds

        # Check time threshold.
        if motion and timeDelta > conf["max_vid_time"]:
            # Send notification if no notification sent.
            if not sent:
                msg = "Motion detected."

                # Release the video writer pointer and reset the writer object.
                writer.release()
                writer = None


                # Send the message and the video to the owner and set the notification sent flag.
                print("Sending message...")
                notif.send(msg, cap)
                sent = True

        # Check if no motion in frame.
        elif not motion:

            # Reset sent indicator.
            if sent:
                sent = False

            else:
                # Record time.
                endTime = datetime.now()
                totalSeconds = (endTime - startTime).seconds
                today = date.today().strftime("%A, %B %d %Y")

                # Send notification, reset video.
                msg = "Motion detected for {} seconds on {}".format(totalSeconds, today)
                writer.release()
                writer = None
                print("Sending message...")
                notif.send(msg, cap)

        # Write ongoing captures to disk.
        if writer is not None:
            writer.write(frame)


# Kill processes.
if writer is not None:
    writer.release()
cv2.destroyAllWindows()
vs.stop()
