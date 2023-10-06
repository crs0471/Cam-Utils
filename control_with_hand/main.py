import cv2
import mediapipe as mp
import pyautogui
from itertools import cycle
from time import time, sleep
import tensorflow as tf

class Draw():
    def add_text(self, text, location, font_scale=1, color=(0,255,255), thick_ness=2):
        cv2.putText(self.image, f"{text}", location, cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, (0,255,255), thick_ness)

    def add_circle(self, center, radius=8, color=(255, 0, 255), thickness=2):
        cv2.circle(self.image, center=center, radius=8, color=(255, 0, 255), thickness=2)

    def add_line(self, point1, point2, color=(255, 0, 0), thickness=2):
        cv2.line(self.image, point1, point2, color=color, thickness=thickness)

    def add_line_for_multi_points(self, list_of_points, color=(255, 0, 0), thickness=2):
        if len(list_of_points) > 1:
            for index, current_point in enumerate(list_of_points[:-1]):
                next_point = list_of_points[index + 1]
                self.add_line(current_point, next_point, color=color, thickness=thickness)

class Math():
    @staticmethod
    def find_distance(list_of_points=[]):
        dist = 0
        if len(list_of_points) > 1:
            for index, current_point in enumerate(list_of_points[:-1]):
                next_point = list_of_points[index + 1]
                temp_dist = ((next_point[0] - current_point[0])**2 + (next_point[1] - current_point[1])**2)**0.5 
                dist += temp_dist
        return dist / 4

class Control:  
      
    def change_action(self):
        print('Changing action......')
        self.selected_action = next(self.actions)
        self.time_counter = time()
      
    def volume_up(self):
        print('increasing volume......')
        pyautogui.press("volumeup")
        self.time_counter = time()

    def volume_down(self):
        print('decreasing volume......')
        pyautogui.press("volumedown")
        self.time_counter = time()

    def window_change(self):
        print('change windows')
        pyautogui.hotkey('winleft','tab')
        self.time_counter = time()

    def press_right(self):
        print('pressed right arrow')
        pyautogui.press("right")
        self.time_counter = time()

    def press_tab(self):
        print('pressed tab')
        pyautogui.press("tab")
        self.time_counter = time()

    def press_enter(self):
        print('pressed enter')
        pyautogui.press("enter")
        self.time_counter = time()

    def move_pointer(self):
        print('moving pointer')
        pyautogui.moveTo( self.x, self.y ,duration=1)
        self.time_counter = time()


class Main(Control, Draw):

    def register_action(self, hand_point_list, action, condition, distance_threshold:int, time_threshold=1, in_mode=None):
        self.point_list = []
        if in_mode == None or self.selected_action==in_mode:
            for i in hand_point_list:
                x = int(self.landmarks[i].x * self.frame_width)
                y = int(self.landmarks[i].y * self.frame_height)
                cv2.circle(self.image, center=(x,y), radius=8, color=(255, 0, 255), thickness=2)
                self.point_list.append((x, y))
                self.x = x
                self.y = y

            dist = Math.find_distance(self.point_list)
            self.add_line_for_multi_points(self.point_list)

            if condition == '>' and dist > distance_threshold and self.time_counter + time_threshold < time():
                action()
            elif condition == '<' and dist < distance_threshold and self.time_counter + time_threshold < time():
                action()

        


    def run(self):
        webcam = cv2.VideoCapture(0)
        my_hand = mp.solutions.hands.Hands()
        drawing_utils = mp.solutions.drawing_utils

        action_x1 = action_y1 = action_x2 = action_y2 = 0
        self.time_counter = time()
        self.actions = cycle(['None', 'Volume', 'Windows'])
        self.selected_action = next(self.actions)
        point_list = []

        while True:
            self.point_list = []
            _, image = webcam.read()
            self.image = image
            image = cv2.flip(image, 1)
            image = cv2.resize(image, (960,540))
            self.frame_height, self.frame_width, _ = image.shape
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.putText(image, f"{self.selected_action}", (10, 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,255), 2)
            
            output = my_hand.process(rgb_image)
            hands = output.multi_hand_landmarks
            if (hands):
                # for hand in hands:
                hand = hands[-1]
                drawing_utils.draw_landmarks(image, hand)
                self.landmarks = hand.landmark

                # actions
                if len(hands) > 1:
                    self.register_action([5,6,7,8,9,10,11,12,13], self.change_action, '<', 50, time_threshold=1)

                else:
                    # volume
                    self.register_action([8,4], self.volume_down, '<', 10, in_mode="Volume", time_threshold=1)
                    self.register_action([8,4], self.volume_up, '>', 25, in_mode="Volume", time_threshold=1)

                    # windows
                    self.register_action([8,4], self.window_change, '<', 10, in_mode="Windows", time_threshold=1)
                    self.register_action([12,4], self.press_tab, '<', 10, in_mode="Windows", time_threshold=1)
                    self.register_action([16,4], self.press_right, '<', 10, in_mode="Windows", time_threshold=1)
                    self.register_action([13,4], self.press_enter, '<', 10, in_mode="Windows", time_threshold=1)

                    

            cv2.imshow("Hand Control", image)
            key = cv2.waitKey(10)
            if key == 27:
                break
                
        webcam.release()
        
cv2.destroyAllWindows()
main = Main()
main.run()