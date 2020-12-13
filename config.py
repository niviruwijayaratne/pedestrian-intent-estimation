import os
import os.path as osp

weights_dir = osp.join(os.getcwd(), "weights")
CLASSIFIER_WEIGHTS = osp.join(weights_dir, "classifier.pkl")
POSE_WEIGHTS = osp.join(weights_dir, "coco_pose_iter_440000.pth.tar")
SSD_WEIGHTS = osp.join("..", weights_dir, "detection", "ssd", "weights", "ssd300_mAP_77.43_v2.pth")
