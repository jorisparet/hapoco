import mediapipe as mp
import numpy
import cv2

# Mediapipe shortcuts
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Custom MediaPipe drawing style
# TODO: make a parameter?
#  hand landmarks
landmark_annotations = mp_styles.get_default_hand_landmarks_style()
for landmark in landmark_annotations.keys():
    landmark_annotations[landmark] = mp_drawing.DrawingSpec(color=(150,150,150), thickness=0, circle_radius=0)
#  hand connections
connection_annotations = mp_styles.get_default_hand_connections_style()
for connection in connection_annotations.keys():
    connection_annotations[connection] = mp_drawing.DrawingSpec(color=(150,150,150), thickness=2, circle_radius=1)

def draw_hand_landmarks(image, hand_landmark):
    mp_drawing.draw_landmarks(image, 
        hand_landmark,
        mp_hands.HAND_CONNECTIONS,
        landmark_annotations,
        connection_annotations)

def draw_tracking_center(image, center, color_BGR=(255,255,255), size=0.01):
    height, width, _ = image.shape
    radius = int(size * height)
    center = (center * numpy.array([width, height])).astype(int)
    cv2.circle(image, center, radius, color_BGR, thickness=-1)
    
def draw_cursor_area(image, center, color_BGR=(255,255,255), min_size=0.05, max_size=0.15):
    # TODO: all these calculations can be done only once
    # The resulting overlay can be stored in memory and reused at every frame
    height, width, _ = image.shape
    center = (center * numpy.array([width, height])).astype(int)
    radius_min = int(min_size * height)
    radius_max = int(max_size * height)
    cv2.circle(image, center, radius_min, color_BGR, thickness=2)
    cv2.circle(image, center, radius_max, color_BGR, thickness=2)

def draw_action_area(image, center, color_BGR=(255,255,255), min_size=0.05, max_size=0.15):
    # TODO: all these calculations can be done only once
    # The resulting overlay can be stored in memory and reused at every frame
    height, width, _ = image.shape
    center = (center * numpy.array([width, height])).astype(int)
    radius_min = int(min_size * height)
    radius_max = int(max_size * height)
    # Circles
    cv2.circle(image, center, radius_min, color_BGR, thickness=2)
    cv2.circle(image, center, radius_max, color_BGR, thickness=2)
    # Quarters
    # TODO: the end points of the lines do not coincide well with the circles
    shifted_radius = radius_max - 2 * radius_min # TODO: why is this factor 2 necessary?
    bottom_left = (center[0] - shifted_radius, center[1] - shifted_radius)
    top_right = (center[0] + shifted_radius, center[1] + shifted_radius)
    bottom_right = (center[0] + shifted_radius, center[1] - shifted_radius)
    top_left = (center[0] - shifted_radius, center[1] + shifted_radius)
    cv2.line(image,
             (center[0]+radius_min, center[1]+radius_min),
             top_right,
             color_BGR,
             thickness=2)
    cv2.line(image,
             (center[0]+radius_min, center[1]-radius_min),
             bottom_right,
             color_BGR,
             thickness=2)
    cv2.line(image,
             (center[0]-radius_min, center[1]+radius_min),
             top_left,
             color_BGR,
             thickness=2)
    cv2.line(image,
             (center[0]-radius_min, center[1]-radius_min),
             bottom_left,
             color_BGR,
             thickness=2)