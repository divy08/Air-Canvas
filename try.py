import cv2
import time
import HandTracker as ht
import cvzone
from pynput.keyboard import Controller
import numpy as np


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = ht.handDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                      (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    # print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


class MyButton:
    pos = [0, 0]
    text = ""
    size = [85, 85]

    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(MyButton(pos=[100 * j + 50, 100 * i + 50], text=key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            # print(button.pos)
            x, y = button.pos
            w, h = button.size
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            # l = detector.findPosition(img)
            # print(l)

            ## when clicked
            # if l[0][0] < 30:
            #     keyboard.press(button.text)
            #     cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
            #     cv2.putText(img, button.text, (x + 20, y + 65),
            #                 cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            #     # print(button.text)
            #     #TODO: Make a map of areas of keys
            #     finalText += button.text
            #     print(finalText)
            #     time.sleep(1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


# print(finalText)
        # sleep(0.15)

# cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
# cv2.putText(img, finalText, (60, 430),
#             cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
# pTime = 0
# cTime = 0
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
#
# detector = ht.handDetector(detectionCon=0.8)
# while True:
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList = detector.findPosition(img)
#     # if len(lmList) != 0:
#     #     print(lmList[8])
#     cv2.rectangle(img,(100,100),(200,200),(255,0,255),cv2.FILLED)
#     cv2.putText(img,"Q", (120,175), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
#
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#
#     cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
#
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)


# def drawAll(img, buttonList):
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#         cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 20, y + 65),
#                     cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#     return img