import cv2
import numpy as np
import os
from PIL import Image
import sys

# camera_utils
version_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, f"{version_dir}/weld_camera/src")
from camera_sdk.camera_util import read_exr_to_array, save_array_to_exr

def apply_threshold(thread,img):
    thread = thread
    img[img > thread] = 255
    img[img <= thread] = 0
    return img

def get_rmtx(rvec):
    check_rvec(rvec)
    rmtx, _ = cv2.Rodrigues(rvec)
    rmtx = np.matrix(rmtx)
    check_rmtx(rmtx)
    return rmtx

def get_rvec(rmtx):
    check_rmtx(rmtx)
    rvec, _ = cv2.Rodrigues(rmtx)
    rvec = np.matrix(rvec)
    check_rvec(rvec)
    return rvec

def InvTransformRT(R, T):
    check_rmtx(R)
    check_tvec(T)

    R_inv = R.T
    T_inv = -R_inv * T

    return R_inv, T_inv

def check_tvec(tvec):
    assert tvec.__class__.__name__ == 'matrix'
    assert tvec.ndim == 2
    assert tvec.shape == (3, 1)
    assert tvec.dtype == np.float32 or tvec.dtype == np.float64

def check_rvec(rvec):
    assert rvec.__class__.__name__ == 'matrix'
    assert rvec.ndim == 2
    assert rvec.shape == (3, 1)
    assert rvec.dtype == np.float32 or rvec.dtype == np.float64

def check_rmtx(rmtx):
    assert rmtx.__class__.__name__ == 'matrix'
    assert rmtx.ndim == 2
    assert rmtx.shape == (3, 3)
    assert rmtx.dtype == np.float32 or rmtx.dtype == np.float64

def get_rvec_Yaskawa(rx, ry, rz):   ## 欧拉角到旋转矩阵
    euler_angle = [rx, ry, rz]
    rmtx = R.from_euler('xyz', euler_angle, degrees=True).as_matrix()
    rmtx = np.matrix(rmtx, dtype=np.float32)
    rvec, _ = cv2.Rodrigues(rmtx)   # 旋转矩阵R返回旋转向量
    rvec = np.matrix(rvec)

    check_rvec(rvec)
    return rvec

def Loading_Depth_From_Png(depth_file):
    # depth = cv2.imread(depth_file, -1)
    # depth=depth/65536*1300
    # depth = np.float32(np.array(depth))
    depth = read_exr_to_array(depth_file)

    return depth

def interp2d(image, point):
    x = point[0]
    y = point[1]

    x0 = int(x)
    x1 = int(x + 1)
    y0 = int(y)
    y1 = int(y + 1)

    x0_weight = x - x0
    x1_weight = x1 - x
    y0_weight = y - y0
    y1_weight = y1 - y

    value = image[y0, x0] * y1_weight * x1_weight + \
            image[y1, x0] * y0_weight * x1_weight + \
            image[y1, x1] * y0_weight * x0_weight + \
            image[y0, x1] * y1_weight * x0_weight
    return value


# get Transform from pc2 to pc1 R * pc2 + t = pc1
# numpy version
#   pc1: np.array  [N, 3]
#   pc2: np.array  [N, 3]
def svdICP(pc1, pc2):
    pc1Center = pc1.mean(axis=0)
    pc2Center = pc2.mean(axis=0)
    pc1Centered = pc1 - pc1Center
    pc2Centered = pc2 - pc2Center
    # batch matrix multiplication using broadcasting
    # print("svd测试!!!", pc2Centered[:, :, None])
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

def Get_Board2Cam_Transform_2D(color_img_path, camera_mtx, camera_dist):
    # print("Using 2D-3D to compute the Transform Matrix between Board and Camera")
    objectpoints = CircleObjectPointsGenerate(7, 9, 25, 25)  #11->9
    color_img = cv2.imread(color_img_path, 0)
    color_img = 255 - color_img
    ret, centers = cv2.findCirclesGrid(color_img, (7, 9), flags=cv2.CALIB_CB_SYMMETRIC_GRID)

    # _, rvec, tvec = cv2.solvePnP(objectpoints, centers, camera_mtx, camera_dist)
    _, rvec, tvec = cv2.solvePnP(objectpoints, centers, camera_mtx, camera_dist)
    rmtx = get_rmtx(np.matrix(rvec))
    tvec = np.matrix(tvec)
    check_rmtx(rmtx)
    check_tvec(tvec)

    return rmtx, tvec

def Get_Board2Cam_Transform_3D(color_img_path, depth_img_path, camera_mtx, camera_dist):
    # print("Using 3D-3D to compute the Transform Matrix between Board and Camera")
    objectpoints = CircleObjectPointsGenerate(7, 9, 25, 25)
    color_img = cv2.imread(color_img_path, 0)
    color_img = cv2.undistort(color_img, camera_mtx, camera_dist)
    # color_img = apply_threshold(100,color_img) #二值化
    color_img = 255 - color_img #反转颜色
    image = Image.fromarray(color_img)
    txt_filename = f"{os.path.splitext(color_img_path)[0]}_settled.bmp"
    image.save(txt_filename)
    a = color_img.shape
    print(a)
    # color_img = cv2.resize(color_img,(int(a[1]/1.5),int(a[0]/1.5)))
    params = cv2.SimpleBlobDetector_Params()
    # params.filterByArea = True
    # params.minArea = 1000
    # params.maxArea = 15000
    params.filterByColor = True
    params.blobColor = 0
    detector = cv2.SimpleBlobDetector_create(params)
    ret, centers = cv2.findCirclesGrid(color_img, (9, 7), flags=cv2.CALIB_CB_SYMMETRIC_GRID, blobDetector=detector)
    print(centers.shape)
    print("ret: {}".format(ret))
    print(len(centers))
    #print(centers)
    for i in centers:
        cv2.circle(color_img,(int(i[0][0]),int(i[0][1])),8,(255,255,255),6) 
    txt_filename = f"{os.path.splitext(color_img_path)[0]}_settled.bmp"
    image = Image.fromarray(color_img)
    image.save(txt_filename)

    depth = Loading_Depth_From_Png(depth_img_path)
    print(depth.shape)
    # depth = Depth_Middle_Fliter(depth)
    # Filter is needed for depth?
    # centers_undistort = cv2.undistortPoints(centers, camera_mtx, camera_dist, None, camera_mtx)
    centers_undistort = centers
    # print(centers)
    centers_3d = []
    fx = camera_mtx[0][0]
    fy = camera_mtx[1][1]
    cx = camera_mtx[0][2]
    cy = camera_mtx[1][2]
    print(camera_mtx)
    for i in range(len(centers)):
        points = centers_undistort[i, 0, :]
        # print(i)
        # print(points)
        z = interp2d(depth, points)
        # print(z)
        # x = centers_undistort[i, 0, 0] * z
        x = (centers_undistort[i, 0, 0] - cx) * z / fx
        # y = centers_undistort[i, 0, 1] * z
        y = (centers_undistort[i, 0, 1] - cy) * z / fy
        pts = np.array([x, y, z])
        centers_3d.append(pts)
    centers_3d = np.array(centers_3d)
    # print(centers_3d.shape)
    try:
        rmtx, tvec = svdICP(centers_3d, objectpoints)
        # rmtx = np.matrix(rmtx)
        # tvec = np.matrix(tvec.reshape(3, 1))
        # cam2board_rmtx, cam2board_tvec = InvTransformRT(rmtx, tvec)
        # centers_3d = np.matrix(centers_3d).T
        # centers_3d = cam2board_rmtx * centers_3d + cam2board_tvec
        # centers_3d = np.array(centers_3d).T
        # rmtx, tvec = svdICP(centers_3d, objectpoints)
    except Exception as e:
        print(f"该拍照位姿未识别出标定板。图片路径:{color_img_path}, 错误代码为:{e}")
    rmtx = np.matrix(rmtx)
    tvec = np.matrix(tvec.reshape(3, 1))
    check_tvec(tvec)
    check_rmtx(rmtx)
    # print(centers_3d)
    #计算误差
    cam2board_rmtx, cam2board_tvec = InvTransformRT(rmtx, tvec)
    # print(cam2board_rmtx,cam2board_tvec)
    centers_3d_board = np.matrix(centers_3d).T
    centers_3d_board = cam2board_rmtx * centers_3d_board + cam2board_tvec
    centers_3d_board = np.array(centers_3d_board).T
    print('-------------------------------------------------------')
    # print(centers_3d_board)
    print('-------------------------------------------------------')
    # print(objectpoints)
    error_list = np.linalg.norm(centers_3d_board - objectpoints, axis=1, keepdims=True)
    print("Current error when transform centers from Camera to Board:", np.mean(error_list))
    return rmtx, tvec, error_list, centers_3d

def Loading_Params_From_Txt(params_file):
    params = np.loadtxt(params_file)
    camera_mtx = np.zeros((3, 3))
    camera_mtx[0, 0] = params[0]
    camera_mtx[0, 2] = params[2]
    camera_mtx[1, 1] = params[4]
    camera_mtx[1, 2] = params[5]
    camera_mtx[2, 2] = 1
    camera_dist = params[9:14]

    return camera_mtx, camera_dist

def CircleObjectPointsGenerate(xNum, yNum, xSpace, ySpace):
    objectpoints = []
    for j in range(xNum):
        for i in range(yNum):
            if j % 2 == 0:
                x = i * xSpace
            else:
                # x = (i + 0.5) * xSpace
                x = i * xSpace *1.0
            y = j * ySpace
            z = 0
            objectpoint = np.array([x, y, z])
            objectpoints.append(objectpoint)
    objectpoints = np.array(objectpoints)

    return objectpoints

if __name__ == '__main__':
    # calib()

    # data_path = "cloud/"
    # file_json_path = "file.json"
    # pos_json_path = "pos.json"
    # param_txt_path = "param.txt"
    # cam2tcp_json_path = 'cam2tcp.json'
    # new_base_cloud_path='new_base_cloud'

    # cam2tcp_rvec, cam2tcp_tvec = load_transform(cam2tcp_json_path)
    # cam2tcp_rmtx = get_rmtx(cam2tcp_rvec)

    # camera_mtx, camera_dist = Loading_Params_From_Txt(param_txt_path)

    # # 这个函数是生成无畸变的在极坐标系下的三维点云图：
    # New_Generate_Pointclouds(data_path, cam2tcp_rmtx, cam2tcp_tvec, camera_mtx,
    #                          camera_dist,new_base_cloud_path)
    color_img_path = '/home/yofo/version/weld_calib_sdk/data/cloud/pos0/pos0.bmp'
    depth_img_path = '/home/yofo/version/weld_calib_sdk/data/cloud/pos0/pos0.exr'
    param_txt_path = '/home/yofo/version/weld_calib_sdk/data/cam_param.txt'
    camera_mtx, camera_dist = Loading_Params_From_Txt(param_txt_path)
    Get_Board2Cam_Transform_3D(color_img_path, depth_img_path, camera_mtx, camera_dist)
