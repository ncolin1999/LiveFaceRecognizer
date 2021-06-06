import os
import torch
from facenet_pytorch import MTCNN,InceptionResnetV1
import cv2
import numpy as np
import pickle
import threading
import imutils
from imutils.video import VideoStream
import multiprocessing
from threading import Lock
import time
import pandas as pd
import os


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(device)
device  = 'cpu'
mtcnn = MTCNN(keep_all=True,device=device)
resnet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

df = pd.read_csv(os.path.join(os.getcwd(),"recognizer/unique_face_embedding.csv"))
subdf = df[df.columns[:-1]].to_numpy()
def recognize(rgb):
    faces =     mtcnn(rgb)
    if faces is not None and len(faces)==1:
            embedings = resnet(faces).detach().cpu().numpy()
            for e in embedings:
                d =[]
                for i,encoding in enumerate(subdf):
                    r = np.linalg.norm(encoding-e)
                    d.append((r,i))
                d = min(d)
                print(d)
                if d[0]>0.75:
                    pass
                else:
                    return df.iloc[d[1],-1]
                    
    else:
        return "too many faces or no face found"