import cv2
import mediapipe as mp
import pyautogui
import argparse

from hapoco.filter import OneEuroFilter
from hapoco.hand import Hand
from hapoco.controllers import ActionController, CursorController
from hapoco.overlay import draw_hand_landmarks, draw_tracking_center, draw_cursor_area, draw_action_area

# Mediapipe shortcut
mp_hands = mp.solutions.hands

# Allow mouse to go on the border of the screen
pyautogui.FAILSAFE = False

# Window name for the video feed
__window_name__ = "Hapoco preview"

def main():

    # Parser
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    description = f"""{parser.prog} activates the webcam and allows to use both hands
    to take control of the mouse cursor and perform several basic actions, such as
    left click, right click, drag and drop and scrolling. The main hand controls the
    motion of the cursor and the other hand controls its actions.""".replace('\n',' ')
    parser.description = description
    parser.add_argument('-m', '--main_hand',
                        default='right',
                        choices=['left', 'right'],
                        type=str,
                        help='Hand used to control the cursor')
    parser.add_argument('-v', '--view',
                        default='down',
                        choices=['down', 'front'],
                        type=str,
                        help='Camera view ("down": camera looks down, "front": camera faces the user)')
    parser.add_argument('-or', '--origin_right',
                        default=(0.75, 0.50),
                        nargs='+',
                        type=float,
                        help='Coordinates of the control area of the right hand')
    parser.add_argument('-ol', '--origin_left',
                        default=(0.25, 0.50),
                        nargs='+',
                        type=float,
                        help='Coordinates of the control area of the left hand')
    parser.add_argument('-smin', '--sensitivity_min',
                        default=1,
                        type=int,
                        help='Mouse sensitivity at the lower edge of the motion area')
    parser.add_argument('-smax', '--sensitivity_max',
                        default=15,
                        type=int,
                        help='Mouse sensitivity at the upper edge of the motion area')
    parser.add_argument('-rmin', '--radius_min',
                        default=0.03,
                        type=float,
                        help='Minimum radius below which no action is performed')
    parser.add_argument('-rmax', '--radius_max',
                        default=0.2,
                        type=float,
                        help='Maximum radius above which no action is performed')
    parser.add_argument('-sc', '--scrolling_speed',
                        default=1,
                        type=int,
                        help='Scrolling speed')
    parser.add_argument('--show',
                        action='store_true',
                        help='Real-time display of the processed camera feed')
    parser.add_argument('-t', '--tracking_landmarks', 
                        default=[0,5,9,13,17],
                        nargs='+',
                        type=int,
                        help='Hand landmarks to use for tracking')
    parser.add_argument('-d', '--device',
                        default=0,
                        type=int,
                        help='Camera device index to be used')
    args = parser.parse_args()
    # Custom variables linked to parser
    main_hand = args.main_hand
    view = args.view
    origin_right = args.origin_right
    origin_left = args.origin_left
    sensitivity_min = args.sensitivity_min
    sensitivity_max = args.sensitivity_max
    radius_min = args.radius_min
    radius_max = args.radius_max
    scrolling_speed = args.scrolling_speed
    show_feed = args.show
    tracking_points = args.tracking_landmarks
    device = args.device

    # Filter
    # TODO: maybe not needed? Leave it for later just in case
    # min_cutoff_filter = 0.01 
    # beta_filter = 10.0 
    # motion_smoothing = [OneEuroFilter(0.0, 0.0, min_cutoff=min_cutoff_filter, beta=beta_filter) for _ in range(2)]

    # Controllers
    cursor_controller = CursorController(sensitivity_min=sensitivity_min,
                                         sensitivity_max=sensitivity_max,
                                         radius_min=radius_min,
                                         radius_max=radius_max)
    action_controller = ActionController(radius_min=radius_min,
                                         radius_max=radius_max,
                                         scrolling_speed=scrolling_speed)

    # View
    sides = ['left', 'right']
    if view == 'down':
        flip = -1
        switch_prediction = True
    if view == 'front':
        flip = 1
        switch_prediction = False

    # Main hand
    right_controller, left_controller = None, None
    if main_hand == 'right':
        right_controller = cursor_controller
        left_controller = action_controller
    if main_hand == 'left':
        right_controller = action_controller
        left_controller = cursor_controller
    # Controllers' origins
    right_controller.origin = origin_right
    left_controller.origin = origin_left

    # Webcam input
    capture = cv2.VideoCapture(device)
    with mp_hands.Hands(static_image_mode=False,
                        model_complexity=1,
                        max_num_hands=2,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:
        
        # Detect hand movement while the video capture is on
        while capture.isOpened():
            success, image = capture.read()
            image = cv2.flip(image, flip)
            # TODO: find a way to do it only once
            cursor_controller.set_cam_aspect_ratio(image)
            action_controller.set_cam_aspect_ratio(image)

            # A hand is detected
            results = hands.process(image)
            hand_detected = bool(results.multi_hand_landmarks)
            if hand_detected:

                # Handle both hands
                for h_idx, h in enumerate(results.multi_handedness):
                    
                    h_label = h.classification[0].label # TODO: this index makes no sense...
                    # TODO: below is not very elegant
                    # switch the predicted hand left <--> right for view "down" due to the image inversion
                    if switch_prediction:
                        h_label = sides[1 - sides.index(h_label.lower())]
                    h_landmarks = results.multi_hand_landmarks[h_idx].landmark
                    hand = Hand(h_label, h_landmarks, tracking_points=tracking_points)

                    # Operate
                    if hand.label == 'right':
                        right_controller.operate(hand.tracking_center)

                    if hand.label == 'left':
                        left_controller.operate(hand.tracking_center)

                    # Draw landmarks
                    draw_hand_landmarks(image, results.multi_hand_landmarks[h_idx])
                    draw_tracking_center(image, hand.tracking_center, color_BGR=(0,255,0), size=0.01)

            # Draw control areas
            # TODO: make a parameter?
            color = (0,0,255)
            draw_cursor_area(image, cursor_controller.origin, min_size=radius_min, max_size=radius_max, color_BGR=color)
            draw_action_area(image, action_controller.origin, min_size=radius_min, max_size=radius_max, color_BGR=color)

            # Show the camera feed
            if show_feed:

                # Show
                cv2.imshow(__window_name__, image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break

if __name__ == '__main__':
    main()