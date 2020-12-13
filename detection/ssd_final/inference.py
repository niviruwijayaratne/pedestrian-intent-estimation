import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
import numpy as np
import cv2
if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
sys.path.append(os.getcwd() + "/detection/ssd_final/")
from data import VOC_CLASSES as labels


class Detector():
    def __init__(self, model):
        self.model = model


    def preprocess(self, frame):
        x = cv2.resize(frame, (300, 300)).astype(np.float32)
        x -= (104.0, 117.0, 123.0)
        x = x.astype(np.float32)
        x = x[:, :, ::-1].copy()
        x = torch.from_numpy(x).permute(2, 0, 1)
        frame = x.unsqueeze(0)
        return frame

    def get_bbs(self, frame):
             # wrap tensor in Variable
        preprocessed_frame = self.preprocess(frame)
        if torch.cuda.is_available():
            preprocessed_frame = preprocessed_frame.cuda()
        y = self.model(preprocessed_frame)
        scale = torch.Tensor(frame.shape[1::-1]).repeat(2)
        bboxes = []
        for i in range(y.size(1)):
            j = 0
            while y[0,i,j,0] >= 0.6:
        #         print(i, detections[0, i, j])
                score = y[0,i,j, 0]
                # label_name = labels[i-1]
                # display_txt = '%s: %.2f'%(label_name, score)
                if labels[i - 1] != "person":
                    j += 1
                    continue
                bboxes.append((y[0,i,j,1:]*scale).cpu().detach().numpy())
                j += 1
        return bboxes

    
