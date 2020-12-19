import os

# WEIGHTS_PATH = os.path.join("/home/ubuntu/niviru/poseflow-pie/pose_estimation", "utils", "coco_pose_iter_440000.pth.tar")
WEIGHTS_PATH = os.getcwd() + "/utils/coco_pose_iter_440000.pth.tar"
RESULTS_PATH = os.path.join("/home/ubuntu/niviru/poseflow-pie/Pose Estimation", "utils", "assets", "results")
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 2
NECK = 1
LEFT_HIP = 11
RIGHT_HIP = 8
LEFT_KNEE = 12
RIGHT_KNEE = 9
LEFT_ANKLE = 13
RIGHT_ANKLE = 10
KEYPOINTS = [5, 2, 1, 11, 8, 12, 9, 13, 10]



