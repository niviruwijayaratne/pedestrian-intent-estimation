import numpy as np
import argparse
import cv2
from pose_estimation.pose_estimation import img_inference
from detection.ssd_final.inference import Detector
from detection.ssd_final.ssd import build_ssd
import os
import pickle
from config import *


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rf_weights", help="path to classifier", default= CLASSIFIER_WEIGHTS)
    ap.add_argument("--ssd_weights", help="path to ssd weights", default= SSD_WEIGHTS)
    ap.add_argument("--input", help="path to video")
    ap.add_argument("--output", help="path to output", default="results/")
    args = vars(ap.parse_args())

    ssd = build_ssd('test', 300, 21)    # initialize SSD
    ssd.load_weights(args.ssd_weights)
    detector = Detector(ssd)
    vid = cv2.VideoCapture(args.input)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
    frame_count = {}
    ped_features = {}
    classifier = pickle.load(args.rf_weights)
    while True:
        ret, frame = vid.read()
        if ret:
            bboxes = detector.get_bbs(frame)
            for i, bbox in enumerate(bboxes):
                frame, features = img_inference(frame, bbox)
                frame_count["pedestrian" + str(i)] = 1 + frame_count.get("pedestrian" + str(i), 0)
                if ped_features["pedestrian" + str(i)]:
                    if len(ped_features["pedestrian" + str(i)] >= 5544):
                        if classifier.predict(ped_features["pedestrian" + str(i)]):
                            frame = cv2.putText(frame, "C", (bbox[0], bbox[1]), "FONT_HERSHEY_PLAIN", (0, 255, 0), 1)
                        else:
                            frame = cv2.putText(frame, "NC", (bbox[0], bbox[1]), "FONT_HERSHEY_PLAIN", (0, 0, 255), 1)
                        past_frames = frame_count["pedestrian" + str(i)] - 14
                        ped_features["pedestrian" + str(i)] = np.append(ped_features["pedestrian" + str(i)][396*past_frames: ], features)
                    else:    
                        ped_features["pedestrian" + str(i)] = np.append(ped_features["pedestrian" + str(i)], features)
                else:
                    ped_features["pedestrian" + str(i)] = features
                frame = cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 1)
            out.write(frame)
        else:
            break
    vid.release()
    out.release()

if __name__ == "__main__":
    main()