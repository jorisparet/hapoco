import enum
import numpy

class Hand:

    def __init__(self, label, landmarks, tracking_points=[0,5,9,13,17]):
        self.label = label.lower()
        self.tracking_points = tracking_points
        self.vertices = self._landmarks_to_matrix(landmarks)

    def _landmarks_to_matrix(self, landmarks):
        matrix = numpy.empty((len(landmarks), 2))
        for lm_i, lm in enumerate(landmarks):
            matrix[lm_i] = lm.x, lm.y
        return matrix
    
    @property
    def tracking_center(self):
        return self.vertices[self.tracking_points].mean(axis=0)