import numpy 
import pyautogui

class HandController:

    def __init__(self, origin=(0.5, 0.5), radius_min=0.05, radius_max=0.20, filter=None):
        self.origin = origin
        self.radius_min = radius_min
        self.radius_max = radius_max
        self.filter = filter
        self.screen_resolution = numpy.array(pyautogui.size())
        self.cam_aspect_ratio = None

    def set_cam_aspect_ratio(self, image):
        """
        Aspect ratio of the camera.
        """
        h, w, _ = image.shape
        self.cam_aspect_ratio = w / h


    def _hand_to_screen_coordinates(self, hand_coordinates):
        return hand_coordinates * self.screen_resolution
