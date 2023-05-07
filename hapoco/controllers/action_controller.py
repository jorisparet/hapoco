import numpy
import pyautogui

from .controller import HandController

class ActionController(HandController):

    def __init__(self, origin=(0.25, 0.5), radius_min=0.05, radius_max=0.20, scrolling_speed=1, filter=None):
        HandController.__init__(self, origin=origin, radius_min=radius_min, radius_max=radius_max, filter=filter)
        self.left_down = False
        self.active_right_click = False
        self.scrolling_speed = scrolling_speed

    def operate(self, center):
        vec_origin_to_center = center - self.origin
        vec_origin_to_center[0] *= self.cam_aspect_ratio
        dist_origin_to_center = numpy.linalg.norm(vec_origin_to_center)
        if self.radius_min < dist_origin_to_center < self.radius_max:
            x, y = vec_origin_to_center
            if x < 0 and abs(y) < abs(x):
                if not self.left_down:
                    pyautogui.mouseDown(button='left', _pause=False)
                    self.left_down = True
            if x > 0 and abs(y) < x:
                if not self.active_right_click:
                    pyautogui.rightClick(_pause=False)
                    self.active_right_click = True
            if y > 0 and abs(x) < y:
                pyautogui.scroll(-self.scrolling_speed, _pause=False)
            if y < 0 and abs(x) < abs(y):
                pyautogui.scroll(self.scrolling_speed, _pause=False)
        # Release any button or click
        else:
            if self.left_down:
                pyautogui.mouseUp(button='left')
                self.left_down = False
            if self.active_right_click:
                self.active_right_click = False