import cv2, time, pandas
from datetime import datetime

# default background frame 
static_frame=None

# list to store all status values
status_list=[None,None]

# list to store all times motion is detected
times=[]

# Create a DataFrame structure with two columns
df=pandas.DataFrame(columns=["Start", "End"])

# create a VideoCapture object
video=cv2.VideoCapture(0)

# warming up the camera
video.read()
time.sleep(1)

while True:

    # capture images
    check, frame = video.read()

    # no motion in the current frame
    status = 0

    # convert img to grayscale
    gray_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # blur the image and remove noise; increases accuracy for processing
    gray_frame=cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # store the first frame of the video
    if static_frame is None:
        static_frame=gray_frame
        # continue to the next iteration of the loop; skip the code below
        continue
    
    # abs difference between the first frame and the current frame
    delta_frame=cv2.absdiff(static_frame, gray_frame)

    # if a value is more than 30, assign it a color of white; returns frame from threshold method
    thresh_frame=cv2.threshold(delta_frame, 30, 225, cv2.THRESH_BINARY)[1]

    # smooth threshold frame
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    # contour detection
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # filter out contours; should only have x pixels per area
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        # change status when contour/object is found
        status = 1
        # create a rectangle around that contour
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,225,0), 3)

    # append the current status to the status list
    status_list.append(status)

    # keep two relevant data points and remove the remaining; saves memory
    status_list = status_list[-2:]
    
    # check the status list to see if a motion was detected; change from 0-1 or 1-0
    if status_list[-1]==1 and status_list[-2]==0:
        # record the time that the change occured
        times.append(datetime.now())
    elif status_list[-1]==0 and status_list[-2]==1:
        # record the time that the change occured
        times.append(datetime.now())
    else:
        pass

    # Prepare and resize all windows
    cv2.namedWindow('Gray frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Gray frame', 450, 300)

    cv2.namedWindow('Delta frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Delta frame', 450, 300)

    cv2.namedWindow('Threshold frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Threshold frame', 450, 300)

    cv2.namedWindow('Color frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Color frame', 450, 300)

    # Display all windows
    cv2.imshow("Gray frame", gray_frame)
    cv2.imshow("Delta frame", delta_frame)
    cv2.imshow("Threshold frame", thresh_frame)
    cv2.imshow("Color frame", frame)

    # allow image to be captured every 1ms
    key=cv2.waitKey(1)
    #print(gray)

    # break whileloop if 'q' pressed
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break
    
    print(status)
    # print(gray_frame)
    # print(delta_frame)

print(status_list)
print(times)
# print(static_frame)

# append our motion data to our data frame df
for i in range(0, len(times), 2):
    df=df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

# write our df to a .csv file
df.to_csv("Times.csv")

# release the camera from the script
video.release()
cv2.destroyAllWindows()
