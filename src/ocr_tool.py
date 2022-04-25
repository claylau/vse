import time
from paddleocr import PaddleOCR
import cv2
import sys
from PIL import ImageGrab
import numpy as np
import Levenshtein
from PyQt5.QtCore import QThread
import langid

from utils import *

import os.path
USERDIR = os.path.expanduser('~')

class OcrThread(QThread):
    def __init__(self):
        super().__init__()
        self.img = None
        self.last_subtitle = "Starting 开始"
        self.capture_window = Box()
        self.ocr = PaddleOCR(
            det_model_dir=USERDIR+"/.paddleocr/whl/det/ch/ch_PP-OCRv2_det_infer",
            cls_model_dir=USERDIR+"/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer",
            rec_model_dir=USERDIR+"/.paddleocr/whl/rec/ch/ch_PP-OCRv2_rec_infer",
            use_angle_cls=True, lang='ch', show_log=False)
        self.mode = "desktop"
        self.interval = 1.0
        self.isRunning = False
        self.isPaused = False
        self.fout = sys.stdout
        self.filename = None
        self.lang = []
    
    def onUpdateParam(self, param):
        for k, v in param.items():
            assert k in ("isRunning", "isPaused", "mode", "interval", "filename", "lang")
            self.__setattr__(k, v)
    
    def extract_subtitles(self):
        if self.mode == "desktop":
            self.capture_window = set_screen_window()
            self.extract_desktop_video_subtitles()
        elif self.mode == "video":
            self.capture_window = set_video_window(self.filename)
            self.extract_offline_video_subtitles()
        elif self.mode == "image":
            self.extract_offline_image_subtitles()
        else:
            print(f"{self.mode} not be impletmented yet.")
    
    def extract_offline_image_subtitles(self):
        res = self.ocr.ocr(self.filename, cls=True)
        subtitles = []
        for line in res:
            subtitles.append(line[1][0])
        subtitles_str = " ".join(subtitles)
        print(subtitles_str, file=self.fout)

    def extract_offline_video_subtitles(self):
        if not self.capture_window:
            return 
        cap = cv2.VideoCapture(self.filename)
        cap_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        x1, y1, x2, y2 = self.capture_window.to_tlbr()
        frame_interval = int(self.interval * cap_fps)
        while cap.isOpened():
            if not self.isRunning:
                break
            if self.isPaused:
                time.sleep(1)
                continue
            ret, self.img = cap.read()
            if not ret:
                break
            frame_count += 1
            if frame_count % frame_interval == 0:
                frame_count = 0
                if self.capture_window:
                    cap_img = self.img[y1:y2, x1:x2]
                    self.do_ocr(cap_img)
                else: break
        cap.release()

    def extract_desktop_video_subtitles(self):
        if not self.capture_window:
            return
        box = self.capture_window.to_tlbr()
        while True:
            if not self.isRunning:
                break
            if self.isPaused:
                time.sleep(1)
                continue
            cap_img = np.array(ImageGrab.grab(box))
            cap_img = cv2.cvtColor(cap_img, cv2.COLOR_RGB2BGR)
            self.do_ocr(cap_img)
            if self.interval > 0:
                time.sleep(self.interval)
    
    def do_ocr(self, img):
        res = self.ocr.ocr(img, cls=True)
        subtitles = []
        for line in res:
            txt = line[1][0]
            lang_type = langid.classify(txt)[0]
            if lang_type in self.lang:
                subtitles.append(txt)
        subtitles_str = " ".join(subtitles)
        similarity = Levenshtein.ratio(self.last_subtitle, subtitles_str)
        if similarity < 0.7:
            print(subtitles_str, file=self.fout)
        self.last_subtitle = subtitles_str

    def run(self):
        self.extract_subtitles()