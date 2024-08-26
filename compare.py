import numpy as np
import cv2
import sys
import os
import open3d as o3d
weld_home = os.environ.get('WELD_HOME')
sys.path.append("{}/weld_camera/src".format(weld_home))
from camera_sdk.camera_util import save_array_to_exr, read_exr_to_array

current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = current_dir+'/data/cloud'
intrinsic_path = '/home/yofo/weld_beta_v3/weld_client_cmd/workspace_HFair/near_camK.txt'

def depth_to_pointcloud(depth, cam_K):
    vs, us = depth.nonzero()
    zs = depth[vs, us]
    xs = (us-cam_K[0, 2]) * zs / cam_K[0, 0]
    ys = (vs-cam_K[1, 2]) * zs / cam_K[1, 1]
    pts = np.stack([xs, ys, zs], axis=1)

    return pts

def svdICP(pc1, pc2):
    pc1Center = pc1.mean(axis=0)
    pc2Center = pc2.mean(axis=0)
    print(pc1Center.shape)
    pc1Centered = pc1 - pc1Center
    pc2Centered = pc2 - pc2Center
    print(pc1Centered.shape)
    # batch matrix multiplication using broadcasting
    print("svd测试!!!", pc2Centered[:, :, None].shape)
    # print("svd测试!!!", pc1Centered[:, None, :])
    w = pc2Centered[:, :, None] * pc1Centered[:, None, :]
    w = w.sum(axis=0)
    # print(w)
    u, sigma, vT = np.linalg.svd(w)
    # relativeR = u @ vT
    relativeR = vT.T @ u.T
    detR = np.linalg.det(relativeR)
    if detR < 0:
        vT[2, :] = -vT[2, :]
        relativeR = vT.T @ u.T
    relativeT = pc1Center - (relativeR @ pc2Center[:, None]).reshape(-1)

    return relativeR, relativeT

items = os.listdir(data_path)
directories = [item for item in items if os.path.isdir(os.path.join(data_path, item))]
intrinsic = np.loadtxt(intrinsic_path)
cam2tcp = np.loadtxt('/home/yofo/weld_beta_v3/weld_calib_sdk/data/matrix_cam2tcp_new.txt')
# board2base_current = tcp2base_current_tmp @ cam2tcp_settled @ board2cam_current_tmp

point_clouds = []
points = []
# 创建点云
for i in directories:
    depth_path = data_path+'/'+i+'/'+i+'.exr'
    tcp2base_path = data_path+'/'+i+'/'+'matrix_tcp2base.npy'
    board2cam_path = data_path+'/'+i+'/'+'matrix_board2cam.npy'
    tcp2base = np.load(tcp2base_path)
    board2cam = np.load(board2cam_path)
    
    obj2base = tcp2base @ cam2tcp @ board2cam
    cam2base = tcp2base @ cam2tcp

    obj2camera_depth = read_exr_to_array(depth_path)
    # print(depth_path)
    obj2camera_pointcloud = depth_to_pointcloud(obj2camera_depth, intrinsic)
    # print('------------------------------')
    # print(cam2tcp)
    print(obj2base)
    obj2camera_pointcloud = np.matmul(obj2camera_pointcloud, cam2base[:3, :3].T) + cam2base[:3, 3]
    obj2camera_pc = o3d.geometry.PointCloud()
    obj2camera_pc.points = o3d.utility.Vector3dVector(obj2camera_pointcloud)
    o3d.io.write_point_cloud('/home/yofo/weld_beta_v3/weld_calib_sdk/tmp_data/'+i+'.ply', obj2camera_pc)
    # obj2camera_pc.paint_uniform_color([0,0,1])
    point_clouds.append(obj2camera_pc)

o3d.visualization.draw_geometries(point_clouds)
