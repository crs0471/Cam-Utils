import cv2 
from cvzone.HandTrackingModule import HandDetector
from cvzone import cornerRect, putTextRect
from time import time
        

cap = cv2.VideoCapture(0)
screen_width = 1280
screen_height = 720
cap.set(3, screen_width)
cap.set(4, screen_height)

detector = HandDetector(detectionCon=0.8)

rectangles = []

delete_box = {
    'x' : 0,
    'y' : 0,
    'w' : 200,
    'h' : 200,
    'color' : (0, 0, 255),

}
delete_stack = []

c_rect_w = 100
c_rect_h = 100
tc = time()

while 1:
    success, img = cap.read()
    
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)


    if hands:
        for hand in hands:
            hand_type = hand['type']
            lm_list = hand['lmList']
            center_position = hand['center']
            bbox = hand['bbox']

            if hand_type == "Left":
                distance_8_12, _, _ = detector.findDistance(lm_list[12][0:2], lm_list[8][0:2], img)
                distance_8_4, _, _ = detector.findDistance(lm_list[4][0:2], lm_list[8][0:2], img)
                distance_0_4, _, _ = detector.findDistance(lm_list[0][0:2], lm_list[4][0:2], img)
                rel_distance = (distance_8_12*100)/distance_0_4
                rel_distance_8_4 = (distance_8_4*100)/distance_0_4
                cursor = lm_list[8]
                if rel_distance_8_4 < 20 and tc + 1.5 < time():
                    rectangles.append({
                        'x' : cursor[0],
                        'y' : cursor[1],
                        'color' : (255, 0, 0)
                    })
                    tc = time()

                for rect in rectangles:
                    if rel_distance < 25 and (rect['x']-c_rect_w // 2 < cursor[0] < rect['x'] + c_rect_w // 2) and (rect['y']-c_rect_h // 2 < cursor[1] < rect['y'] + c_rect_h // 2):
                        rect['x'] = cursor[0]
                        rect['y'] = cursor[1]
                        rect['color'] = (0, 255, 0)

                        if (delete_box['x']< cursor[0] < delete_box['x'] + delete_box['w']) and (delete_box['y']< cursor[1] < delete_box['y'] + delete_box['h']):
                            delete_stack.append(rect)
                            print('delete_stack: ', delete_stack)
                                                                                                 


                    else:
                        rect['color'] = (255, 0, 0)

                for rect in delete_stack:
                    rectangles.remove(rect)

                delete_stack = []
    
    for rect in rectangles:
        cv2.rectangle(img, (rect['x']-c_rect_w // 2, rect['y']-c_rect_h // 2),
                    (rect['x'] + c_rect_w // 2, rect['y'] + c_rect_h //2), rect['color'], cv2.FILLED)

    img = cornerRect(img, (delete_box['x'], delete_box['y'], delete_box['w'], delete_box['h']),
                     colorC=delete_box['color'])

    img, _ = putTextRect(img, "Drag Rectangle", (delete_box['x'] + 10, delete_box['y'] + (delete_box['h'] // 2) - 10), 1, 1, (255, 255, 255), delete_box['color'])
    img, _ = putTextRect(img, "here to delete !", (delete_box['x'] + 10, delete_box['y'] + (delete_box['h'] // 2) + 20), 1, 1, (255, 255, 255), delete_box['color'])
    img, _ = putTextRect(img, "Add Rectangle = First Finger + Thumb ", (delete_box['x'] + 10, screen_height - 60), 1, 1, (0, 0, 0), (0, 255, 100))
    img, _ = putTextRect(img, "Pick And Drag Rectangle = First Finger + Second Finger ", (delete_box['x'] + 10, screen_height - 40), 1, 1, (0, 0, 0), (0, 255, 100))

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('image', img)

    key = cv2.waitKey(10)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()