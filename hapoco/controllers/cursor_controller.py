import numpy
import pyautogui

from ..utils import lerp, inv_lerp

from .controller import HandController

class CursorController(HandController):

    def __init__(self, sensitivity_min=1, sensitivity_max=5, origin=(0.75, 0.5), radius_min=0.05, radius_max=0.20, filter=None):
        HandController.__init__(self, origin=origin, radius_min=radius_min, radius_max=radius_max, filter=filter)
        self.sensitivity_min = sensitivity_min
        self.sensitivity_max = sensitivity_max

    def operate(self, center):
        vec_origin_to_center = center - self.origin
        vec_origin_to_center[0] *= self.cam_aspect_ratio
        dist_origin_to_center = numpy.linalg.norm(vec_origin_to_center)
        direction = vec_origin_to_center / dist_origin_to_center
        # Move
        if self.radius_min < dist_origin_to_center < self.radius_max:
            t_dist = inv_lerp(self.radius_min, self.radius_max, dist_origin_to_center)
            delta = lerp(self.sensitivity_min, self.sensitivity_max, t_dist)
            delta = (delta * direction).astype(int)
            pyautogui.move(delta[0], delta[1], _pause=False)