import cv2
import HandTrackingModule
import FaceDetectionModule
import numpy as np


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)

detector = HandTrackingModule.handDetector(detectionCon=0.75)
faceDetector = FaceDetectionModule.FaceDetector()

tipIds = [4, 8, 12, 16, 20]


def fingerCount(img):
    img = detector.findHands(img)
    lmList = []
    lmList.append(detector.findPosition(img,handNo=0, draw=False))
    lmList.append(detector.findPosition(img,handNo=1,draw=False))
    totalFingers = 0

    if len(lmList[0]) != 0:
        fingers = []
        if len(lmList[1]) == 21:
            hands = 2
        else:
            hands = 1


        for index in range(hands):
            # Thumb
            if lmList[index][tipIds[0]][1] > lmList[index][tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[index][tipIds[id]][2] < lmList[index][tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        totalFingers = fingers.count(1)

        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    return totalFingers, img, lmList


def findHandFaceLocation(bbox, handLmList):
    if len(handLmList[0]) != 0:
        if len(handLmList[1]) == 21:
            hands = 2
            return "too many hands!"
        else:
            hands = 1

        # print(handLmList[0][9])
        loc = ""

        # compare each hand in frame to the face location
        for index in range(hands):
            upper_x = bbox[0]
            upper_y = bbox[1]
            lower_x = upper_x + bbox[2]
            lower_y = upper_y + bbox[3]
            hand_x = handLmList[index][9][1]
            hand_y = handLmList[index][9][2]

            if hand_y < upper_y:    # y
                loc += "above"
            elif hand_y > lower_y:  # y
                loc += "below"
            if  hand_x < upper_x:    # x
                loc += "right"
            elif hand_x > lower_x:  # x
                loc += "left"
            if loc == "":
                loc = "in face"
        return loc
    return "no hand!"


def getControlSignal(image_bytes,draw = False):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)

    # success, img = cap.read()
    count, img, lmList= fingerCount(img)
    img, bboxs = faceDetector.findFaces(img)

    if len(bboxs) == 1:
        img = cv2.circle(img, (bboxs[0][1][0],bboxs[0][1][1]),1,(255,255,255))
        faceDetector.fancyDraw(img,bboxs[0][1])
        result = findHandFaceLocation(bboxs[0][1],lmList)
    elif bboxs:
        result = "too many faces!"
    else:
        result = "no face!"

    controlSignal = "idle"
    if "above" in result:
        controlSignal = "up"
    elif "below" in result:
        controlSignal = "down"

    if draw:
        cv2.imshow("image",img)
        cv2.waitKey(1)
    return controlSignal


#while True:
#    success, img = cap.read()
#    # print(type(img))
#    print(getControlSignal(img, draw=True))