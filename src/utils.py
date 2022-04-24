import numpy as np
import cv2
from PIL import ImageGrab


class Box:
    def __init__(self, box=(0, 0, 0, 0)) -> None:
        self.x, self.y, self.w, self.h = box
    
    def to_tlbr(self):
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.w, self.y + self.h
        return (x1, y1, x2, y2)

    def __str__(self) -> str:
        return f"Box: {self.x} {self.y} {self.x+self.w} {self.y+self.h}."
    
    def __bool__(self):
        if self.w * self.h != 0:
            return True
        else:
            return False


def mouse_draw_rectangle(event, x, y, flags, param):
    box, window_name, img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        box.x = x
        box.y = y
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        box.w = x - box.x
        box.h = y - box.y
    elif event == cv2.EVENT_LBUTTONUP:
        if box.w < 0: 
            box.x += box.w
            box.w *= -1
        if box.h < 0: 
            box.y += box.h
            box.h *= -1
        cv2.rectangle(img, (box.x, box.y),
                    (box.x+box.w, box.y+box.h), (0, 255, 0), 4)
        cv2.imshow(window_name, img)


def set_screen_window():
    """to set a capture window in full-screen mode.
    Return:
        box (Box): a box window.
    """
    window_name = "Screenshot"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    screen = np.array(ImageGrab.grab()) # hwc
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    box = Box()
    cv2.imshow(window_name, screen)
    cv2.setMouseCallback(window_name, mouse_draw_rectangle, (box, window_name, screen))
    cv2.waitKey(0)
    cv2.destroyWindow(window_name)
    return box


def set_video_window(video_filename):
    """to set a capture window in offline-video mode.
    Return:
        box (Box): a box window.
    """
    window_name = "SetVideoWindow"
    img = None
    box = Box()
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cap = cv2.VideoCapture(video_filename)
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, img)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.setMouseCallback(window_name, 
                mouse_draw_rectangle, 
                (box, window_name, img))
            cv2.waitKey(0) # most import code to set capture window
        if box:
            break
    cap.release()
    cv2.destroyWindow(window_name)
    return box