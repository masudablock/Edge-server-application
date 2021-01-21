import scipy.io
import numpy as np
import pandas as pd
from open3d import *
import os
import glob
from tqdm import tqdm

#Sequence1のみ変換した
sequence_list = sorted(os.listdir("Sequence"))
for i in range(4):
    print("start " + sequence_list[i])
    sequence_in_sequence_list = sorted(os.listdir("Sequence/" + sequence_list[i]))
    mat_data = scipy.io.loadmat("Sequence/" + sequence_list[i] + "/" + sequence_in_sequence_list[1])
    for j in range(1,15,1):
        for frame_number in tqdm(range(mat_data["result"]["LS_%d"%j][0][0][0][0][1].shape[1])):
            array_xyz = mat_data["result"]["LS_%d"%j][0][0][0][0][1][0, frame_number][0][0][8][:, 0:3]
            pcd = PointCloud()
            pcd.points = Vector3dVector(array_xyz)
            write_point_cloud( "LiDAR_data/"+ sequence_list[i] + "/LS_%02.f"%j + "/%04.f.pcd"%frame_number, pcd, write_ascii=True)
