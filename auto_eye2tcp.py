import sys
import numpy as np
import transforms3d as tfs
import math
import cv2
import os
import shutil
import argparse
import yaml
import datetime
import json

# environment
EYEINHAND = os.environ.get('EYEINHAND')
sys.path.append("{}/weld_client_sdk".format(EYEINHAND))

# calib_sdk
from calib import *

# robot_sdk
sys.path.append("{}/weld_robot/src/robot_sdk/FairAPI".format(EYEINHAND))
from FAIRRobot import FAIRRobotPythonInterface
sys.path.append("{}/weld_robot/src/robot_sdk/DucoCobotAPI".format(EYEINHAND))
from SiasunRobot import SiasunRobotPythonInterface

# camera_sdk
sys.path.append("{}/weld_camera/src/camera_sdk/vsensor".format(EYEINHAND))
from VSensorSDKInterface import VSensorSDKInterface
sys.path.append("{}/weld_camera/src/camera_sdk/guangcheng".format(EYEINHAND))
from GCSDKInterface import GCSDKInterface
sys.path.append("{}/weld_camera/src/camera_sdk/zhiwei".format(EYEINHAND))
from ZhiweiSDKInterface import ZhiWeiInterface
sys.path.append("{}/weld_camera/src/camera_sdk/Ainstec".format(EYEINHAND))
from AinstecInterface import AinstecInterface
sys.path.append("{}/weld_camera/src/camera_sdk/realsense".format(EYEINHAND))
from RealsenseInterface import RealsenseInterface
sys.path.append("{}/weld_camera/src/camera_sdk/tuyang".format(EYEINHAND))
from FS820SDKInterface import FS820SDKInterface

def parse_args():
    parser = argparse.ArgumentParser(description='aiws')
    parser.add_argument('--config_file', default='./config.yaml', type=str)
    args = parser.parse_args()
    with open(args.config_file, "r") as f:
        config_dict = yaml.safe_load(f)
    config = argparse.Namespace(**config_dict)
    # update config file with argparse
    for key,value in args.__dict__.items():
        if value is not None:
            setattr(config, key, value)
    return config

args = parse_args()

service_model = 'local' # cloud or local
if service_model == 'cloud':
    config_path = './config.json'
    from camera_client_sdk import CameraSDK
    camera_sdk = CameraSDK(config_path)
    from robot_client_sdk import RobotSdk
    robot_sdk = RobotSdk(config_path)
elif service_model == 'local':
    print("-----------camera--------------")
    try:
        if args.camera_type =='vsensor':
            camera_sdk = VSensorSDKInterface()
        elif  args.camera_type =='guangcheng':
            camera_sdk = GCSDKInterface()
        elif args.camera_type == 'zhiwei':
            camera_sdk = ZhiWeiInterface()
        elif args.camera_type == 'Ainstec':
            camera_sdk = AinstecInterface()
        elif args.camera_type == 'realsense':
            camera_sdk = RealsenseInterface()
        elif args.camera_type == 'tuyang':
            camera_sdk = FS820SDKInterface()
        
        else:
            print('未找到相机,请检查配置文件config.yaml')
            raise  NotImplemented
    except Exception as e:
        print (f'相机初始化失败，请检查相机连接，错误代码为：{e}')

    print("-----------robot---------------")
    try:
        if args.robot_type == 'fair':
            robot_sdk = FAIRRobotPythonInterface(robot_ip=args.robot_ip)
        elif  args.robot_type == 'siasun':
            robot_sdk = SiasunRobotPythonInterface(robot_ip=args.robot_ip)
        else:
            print('未找到机器人，请检查配置文件config.yaml')
            raise  NotImplemented
    except Exception as e:
        print (f'机器人初始化失败，请检查机器人连接，错误代码为：{e}')

class auto_eye2tcp():
    def __init__(self):
        self.path = "{}/weld_calib_sdk/data".format(EYEINHAND)
        self.param_txt_path = '{}/cam_param.txt'.format(self.path)


        self.camera_mtx, self.camera_dist = Loading_Params_From_Txt(self.param_txt_path)  # 存疑
        
        self.data_path = '{}/cloud/'.format(self.path)
        self.poses_inf = {}
        
        self.cam2tcp_settled_path = '{}/matrix_cam2tcp.txt'.format(self.path)
        self.cam2tcp_settled = np.loadtxt(self.cam2tcp_settled_path).reshape(4, 4)
        self.matrix_cam2eye_new_path = '{}/matrix_cam2tcp_new.txt'.format(self.path)
        
        self.multi_board2cam_current_path = '{}/matrix_board2cam_current.npy'.format(self.path)
        self.multi_tcp2base_current_path = '{}/matrix_tcp2base_current.npy'.format(self.path)
        self.board2base_current_path = '{}/matrix_board2base_current.npy'.format(self.path)
        
        self.cam2borad_settled_path = '{}/cam2borad_settled.json'.format(self.path)
        self.multi_tcp2base_new_path = '{}/matrix_tcp2base_new.json'.format(self.path)
        self.poses_inf_path = '{}/poses_inf.json'.format(self.path)
        
        self.epoch = str(datetime.datetime.now())
        
    def save_npy_and_txt(self, npy_filename, array = np.array([])):
        txt_filename = f"{os.path.splitext(npy_filename)[0]}.txt"
        if array.any():
            np.save(npy_filename, array)
            np.savetxt(txt_filename, array)
        else:
            data = np.load(npy_filename)
            np.savetxt(txt_filename, data)
    
    def clear_folder(self, path):
        """
        path: 指定路径，清除该路径下的所有文件
        """
        folder_to_clear = path

        for item in os.listdir(folder_to_clear):
            item_path = os.path.join(folder_to_clear, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    
    def get_robot_xyz(self):
        """
        得到机器人的xyz坐标信息
        """
        try:
            if service_model == 'local':
                xyz, deg = robot_sdk.get_xyz_eulerdeg()
                xyz_deg = xyz + deg
            else:
                result = robot_sdk.get_xyz_eulerdeg()
                xyz_deg = result['xyz'] + result['eulerdeg']
            return xyz_deg
        except Exception as e:
            print (f'获得当前机器人的xyz坐标信息失败，错误代码为：{e}')
    
    def get_tcp2base_current(self):
        """
        获得当前机器人的tcp2base信息
        return
        tcp2base_current: [x, y, z, rx, ry, rz]
        tcp2base_rmtx: 旋转矩阵3*3
        tcp2base_tvecs: 平移向量 
        """
        try:
            tcp2base_current = robot_sdk.get_RT_matrix()
            tcp2base_current = np.array(tcp2base_current)
            tcp2base_rmtx = tcp2base_current[:3,:3]
            tcp2base_tvecs = tcp2base_current[:3,3]
            return tcp2base_current, tcp2base_rmtx, tcp2base_tvecs
        except Exception as e:
            print (f'获得当前机器人的tcp2base信息失败，错误代码为：{e}')
        
    def move_point(self, target_P):
        """
        traget_P: 目标点,机器人以moveJ的方式移动到目标点
        """
        try:
            robot_sdk.moveJ_pose(target_P)
            return True
        except Exception as e:
            print (f'机器人移动失败，错误代码为：{e}')
            return False

    def take_photo_and_save_data(self, index = 'tmp', method='3D'):
        """
        拍照并存储拍照时的tcp2base信息和board2cam信息
        index: 默认为tmp,信息存储在data/tmp下；指定index时，信息存储在data/cloud中。
        """
        try:
            if index == 'tmp':
                print("当前位姿估计")
                depth_img_path_tmp = '{}/tmp/pos.exr'.format(self.path)
                gray_img_path_tmp = '{}/tmp/pos.bmp'.format(self.path)
                self.tcp2base_tmp_path = '{}/tmp/matrix_tcp2base.npy'.format(self.path)
                self.board2cam_tmp_path = '{}/tmp/matrix_board2cam.npy'.format(self.path)
                
                try:
                    camera_sdk.get_image_gray_and_depth(depth_img_path_tmp, gray_img_path_tmp, exposure_time=90)
                except Exception as e:
                    print (f'拍照失败，请检查相机：{e}')
                    return False,f'拍照失败，请检查相机：{e}'
                tcp2base_current, tcp2base_current_rmtxs, tcp2base_current_tvecs = self.get_tcp2base_current()
                self.save_npy_and_txt(self.tcp2base_tmp_path, tcp2base_current)
                
                try:
                    if method == '3D':
                        
                        board2cam_current_rmtxs, board2cam_current_tvecs, error, centers_3d = Get_Board2Cam_Transform_3D(gray_img_path_tmp, depth_img_path_tmp, self.camera_mtx, self.camera_dist)
                        print("image path: {}".format(gray_img_path_tmp))
                    elif method == '2D':
                        board2cam_current_rmtxs, board2cam_current_tvecs = Get_Board2Cam_Transform_2D(gray_img_path_tmp,  self.camera_mtx, self.camera_dist)
                except Exception as e:
                    print (f'识别标定板失败，请查看图片是否显示完全：{e}')
                    return False,f'识别标定板失败，请查看图片是否显示完全：{e}'
                board2cam_current_tmp = np.zeros((4,4))
                board2cam_current_tmp[:3,:3] = board2cam_current_rmtxs
                board2cam_current_tmp[:3,3] = board2cam_current_tvecs.reshape(3,)
                board2cam_current_tmp[3,3] = 1
                self.save_npy_and_txt(self.board2cam_tmp_path, board2cam_current_tmp)
                
                radians = tfs.euler.mat2euler(tcp2base_current[:3,:3])
                rx, ry, rz = [c*180/math.pi for c in radians]
                folder = "{}/".format(self.path)+str(index)
                np.savetxt(folder+'/point_information.txt',[tcp2base_current[0,3],tcp2base_current[1,3],tcp2base_current[2,3],rx,ry,rz])
                point_information = {}
                point_information['index'] = str(index)
                point_information['epoch'] = self.epoch
                point_information['xyz'] = [tcp2base_current[0,3],tcp2base_current[1,3],tcp2base_current[2,3],rx,ry,rz]
                point_information['error_list'] = error.tolist()
                point_information['centers'] = centers_3d.tolist()
                with open(folder+'/point_information.json',"w",encoding="utf-8") as f:
                    json.dump(point_information, f, indent=2, sort_keys=False, ensure_ascii=False)
                
            else:
                folder = "{}/cloud/pos".format(self.path)+str(index)
                if not os.path.exists(folder):
                    os.mkdir(folder)
                    print(f"文件夹 '{folder}' 已创建。")
                else:
                    print(f"文件夹 '{folder}' 已存在。")
                
                depth_path = folder+"/pos"+str(index)+".exr"
                gray_path = folder+"/pos"+str(index)+".bmp"
                pos_path = folder+"/matrix_tcp2base.npy"
                board2cam_path = folder+"/matrix_board2cam.npy"
                board2base_path = folder+"/matrix_board2base.npy"
                
                try:
                    camera_sdk.get_image_gray_and_depth(depth_path=depth_path, gray_path=gray_path, exposure_time=90)
                    print("image path: {}".format(gray_path))
                except Exception as e:
                    print (f'拍照失败，请检查相机：{e}')
                    return False,f'拍照失败，请检查相机：:{e}'
                tcp2base_current, tcp2base_current_rmtxs, tcp2base_current_tvecs = self.get_tcp2base_current()
                self.save_npy_and_txt(pos_path, tcp2base_current)
                
                try:
                    print("=====before: Get_Board2Cam_Transform===============", method)
                    print("gray_path", gray_path)
                    print("depth_path", depth_path)
                    print("self.camera_mtx", self.camera_mtx)
                    print("self.camera_dist", self.camera_dist)
                    if method == '3D':
                        board2cam_current_rmtxs, board2cam_current_tvecs, error, centers_3d = Get_Board2Cam_Transform_3D(gray_path, depth_path, self.camera_mtx, self.camera_dist)
                    elif method == '2D':
                        board2cam_current_rmtxs, board2cam_current_tvecs = Get_Board2Cam_Transform_2D(gray_path,  self.camera_mtx, self.camera_dist)
                    print("=====finish: Get_Board2Cam_Transform===============", method)
                    board2cam_current = np.zeros((4,4))
                    board2cam_current[:3,:3] = board2cam_current_rmtxs
                    board2cam_current[:3,3] = board2cam_current_tvecs.reshape(3,)
                    board2cam_current[3,3] = 1
                    self.save_npy_and_txt(board2cam_path, board2cam_current)
                    
                    borad2tcp_current = np.dot(self.cam2tcp_settled, board2cam_current)
                    board2base_current = np.dot(tcp2base_current, borad2tcp_current)
                    self.save_npy_and_txt(board2base_path, board2base_current)
                    
                    self.poses_inf[str(index)] = {}
                    self.poses_inf[str(index)]["tcp2base"] = tcp2base_current.tolist()
                    self.poses_inf[str(index)]["tcp2base_rmtxs"] = tcp2base_current_rmtxs.tolist()
                    self.poses_inf[str(index)]["tcp2base_tvecs"] = tcp2base_current_tvecs.tolist()
                    self.poses_inf[str(index)]["board2cam"] = board2cam_current.tolist()
                    self.poses_inf[str(index)]["board2cam_rmtxs"] = board2cam_current_rmtxs.tolist()
                    self.poses_inf[str(index)]["board2cam_tvecs"] = board2cam_current_tvecs.tolist()
                    self.poses_inf[str(index)]["board2base"] = board2base_current.tolist()
                    self.poses_inf[str(index)]["error"] = np.mean(error).tolist()
                    
                    radians = tfs.euler.mat2euler(tcp2base_current[:3,:3])
                    rx, ry, rz = [c*180/math.pi for c in radians]
                    np.savetxt(folder+'/point_information.txt',[tcp2base_current[0,3],tcp2base_current[1,3],tcp2base_current[2,3],rx,ry,rz])
                    point_information = {}
                    point_information['index'] = str(index)
                    point_information['epoch'] = self.epoch
                    point_information['xyz'] = [tcp2base_current[0,3],tcp2base_current[1,3],tcp2base_current[2,3],rx,ry,rz]
                    point_information['error_list'] = error.tolist()
                    point_information['centers'] = centers_3d.tolist()
                    with open(folder+'/point_information.json',"w",encoding="utf-8") as f:
                        json.dump(point_information, f, indent=2, sort_keys=False, ensure_ascii=False)                        
                except Exception as e:
                    print (f'识别标定板失败，请查看图片是否显示完全：{e}')
                    return False,f'识别标定板失败，请查看图片是否显示完全：:{e}'
            return True, np.mean(error)
        except Exception as e:
            print(f'拍照并存储数据失败，错误代码为:{e}')
            return False,f'拍照并存储数据失败，错误代码为:{e}'

    def tcp2base_new(self):
        """
        通过加载相对位姿进行计算新的拍照位姿
        """
        try:
            self.board2cam_current_tmp = np.load(self.board2cam_tmp_path)
            self.tcp2base_current_tmp = np.load(self.tcp2base_tmp_path)

            # board2base_current = tcp2base_current_tmp @ cam2tcp_settled @ board2cam_current_tmp
            self.borad2tcp_current_tmp = np.dot(self.cam2tcp_settled, self.board2cam_current_tmp)
            self.board2base_current = np.dot(self.tcp2base_current_tmp, self.borad2tcp_current_tmp)
            self.save_npy_and_txt(self.board2base_current_path, self.board2base_current)
            
            self.tcp2cam_settled = np.linalg.inv(self.cam2tcp_settled)
            
            self.multi_cam2borad_settled = []
            with open(self.cam2borad_settled_path) as f:
                poses = json.load(f)
            for key in poses.keys():
                self.multi_cam2borad_settled.append(poses[key]["data"])
            self.multi_cam2borad_settled = np.stack(self.multi_cam2borad_settled)
            
            # multi_tcp2base_new = board2base_current @ multi_cam2borad_settled @ tcp2cam_settled
            self.multi_tcp2board_settled = np.einsum('nij,jk->nik', self.multi_cam2borad_settled, self.tcp2cam_settled)
            self.multi_tcp2base_new = np.einsum('ij,njk->nik', self.board2base_current, self.multi_tcp2board_settled)
            
            multi_tcp2base_new = self.multi_tcp2base_new.tolist()
            for key in poses.keys():
                pose = np.array(multi_tcp2base_new.pop(0))
                tran = pose[:3,3].tolist()
                tcp2base_euler = tfs.euler.mat2euler(pose[:3,:3])
                deg = [c/math.pi*180 for c in tcp2base_euler]
                poses[key]["data"] = tran + deg
            
            with open(self.multi_tcp2base_new_path,"w",encoding="utf-8") as f:
                json.dump(poses, f, indent=2, sort_keys=False, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            print(f'加载相对位姿进行计算新的拍照位姿失败，错误代码为:{e}')

    def execute(self):
        """
        利用生成的新的相对位姿，进行拍照并计算新的手眼标定结果
        """
        try:
            with open(self.multi_tcp2base_new_path) as f:
                poses = json.load(f)

            if len(poses.keys()) < 3:
                print('初始化所需信息不够，请重新初始化。')
                return 

            for key in poses.keys():
                result = self.move_point(poses[key]["data"])
                if result:
                    print(poses[key]["data"])
                else:
                    return
                result = self.take_photo_and_save_data(int(key))
                if result:
                    pass
                else:
                    return
                    
            with open(self.poses_inf_path,"w",encoding="utf-8") as f:
                json.dump(self.poses_inf, f, indent=1, sort_keys=False, ensure_ascii=False)

            cam2tcp_new, var, _, _ = self.calib_matrix_cam2tcp()
            cam2tcp_new = f'该次手眼标定结果为:\n{cam2tcp_new.tolist()}'
            print("重投影误差为: ", var)
            print(f'------------------------{datetime.datetime.now()}---------------------------')
            return  cam2tcp_new, var
        except Exception as e:
            print(f'计算新的手眼标定失败，错误代码为:{e}')
        
    def initialize(self):
        """
        第一次设定时，最后初始化相对位姿，保存手眼标定结果供下次计算新手眼标定使用
        """
        try:
            # save poses' tcp2bases and cam2borads
            with open(self.poses_inf_path,"w",encoding="utf-8") as f:
                json.dump(self.poses_inf, f, indent=1, sort_keys=False, ensure_ascii=False)
                f.write('\n')
            
            if len(self.poses_inf.keys()) < 3:
                print('初始化所需的拍照信息不够，应不少于三个，请重新拍照')
                pass

            # save the cam2borad_settled.json   
            poses = {}
            for key in self.poses_inf.keys():
                poses[key] = {}
                poses[key]["data"] = np.linalg.inv(self.poses_inf[key]["board2cam"]).tolist()
            with open(self.cam2borad_settled_path,"w",encoding="utf-8") as f:
                json.dump(poses, f, indent=2, sort_keys=False, ensure_ascii=False)
                f.write('\n')
            
            # calibrate the first matrix_cam2tcp
            self.cam2tcp_settled, var, _, _ = self.calib_matrix_cam2tcp()
            cam2tcp_settled = f'该次手眼标定结果为:\n{self.cam2tcp_settled.tolist()}'
            print("重投影误差为: ", var)
            return cam2tcp_settled, var
        except Exception as e:
            print(f'初始化相对位姿，保存首次手眼标定失败，错误代码为:{e}')
        
    def calib_matrix_cam2tcp(self):
        """
        根据多位资拍照计算手眼标定结果
        """
        try:
            with open(self.poses_inf_path) as f:
                poses = json.load(f)
            
            tcp2base_rmtxs = []
            tcp2base_tvecs = []
            board2cam_rmtxs = []
            board2cam_tvecs = []
            for key in poses.keys():
                tcp2base_rmtxs.append(np.matrix(poses[key]['tcp2base_rmtxs']))
                tcp2base_tvecs.append(np.matrix(poses[key]['tcp2base_tvecs']).reshape(3,1))
                board2cam_rmtxs.append(np.matrix(poses[key]['board2cam_rmtxs']))
                board2cam_tvecs.append(np.matrix(poses[key]['board2cam_tvecs']).reshape(3,1))
            

            cam2tcp_rmtx, cam2tcp_tvec = cv2.calibrateHandEye(tcp2base_rmtxs, tcp2base_tvecs, board2cam_rmtxs, board2cam_tvecs,
                                                        method=cv2.CALIB_HAND_EYE_PARK)
            
            cam2tcp_current = np.zeros((4,4))
            cam2tcp_current[:3,:3] = cam2tcp_rmtx
            cam2tcp_current[:3,3] = cam2tcp_tvec.reshape(3,)
            cam2tcp_current[3,3] = 1
            # print(cam2tcp_current[:3,:3].T @ cam2tcp_current[:3,:3])
            print(cam2tcp_current[:3,:3])
            np.savetxt(self.matrix_cam2eye_new_path,cam2tcp_current)

            board2base_all = []
            for key in poses.keys():
                borad2tcp = np.dot(cam2tcp_current, poses[key]['board2cam'])
                board2base = np.dot(poses[key]['tcp2base'], borad2tcp)
                board2base_all.append(board2base[:3,-1])
            board2base_all = np.array(board2base_all)
            var = np.var(board2base_all,axis=0)
            if var.max()>50:
                var = '该次标定误差过大，请检查机械臂的末端精度、标定过程是否存在标定版移动。'
            else:
                var = f'x轴方向重投影方差为{var[0]}, y轴方向重投影方差为{var[1]}, z轴方向重投影方差为{var[2]}'
            return cam2tcp_current, var, cam2tcp_rmtx, cam2tcp_tvec

        except Exception as e:
            print(f'多位资拍照计算手眼标定结果失败，错误代码为:{e}')
            
    def error_analysis(self):
        sub_dir = [self.data_path+dir.name for dir in os.scandir(self.data_path) if os.path.isdir(dir)]
        error_list = []
        error_list2base = []
        for dir in sub_dir:
            with open(dir+'/point_information.json') as f:
                poses = json.load(f)
            error_list.append(poses['error_list'])
            
            tcp2base = np.load(dir+"/matrix_tcp2base.npy")
            cam2tcp = np.loadtxt(self.matrix_cam2eye_new_path)
            cam2base = tcp2base @ cam2tcp
            points = poses['centers']
            points = np.matmul(points, cam2base[:3, :3].T) + cam2base[:3, 3]
            error_list2base.append(points)
        error_list = np.array(error_list)
        error_list2base = np.array(error_list2base)
        print(error_list.shape)
        error_board = np.hstack((np.max(error_list, axis=0, keepdims=True).squeeze().reshape(63,1),np.min(error_list, axis=0, keepdims=True).squeeze().reshape(63,1)))
        error_base = np.hstack((np.max(error_list2base, axis=0, keepdims=True).squeeze().reshape(63,3),np.min(error_list2base, axis=0, keepdims=True).squeeze().reshape(63,3)))
        error_board_all = np.hstack((error_board,np.var(error_list, axis=0, keepdims=True).squeeze().reshape(63,1)))
        error_base_all = np.hstack((error_base,np.var(error_list2base, axis=0, keepdims=True).squeeze().reshape(63,3)))
        np.savetxt('{}/weld_calib_sdk/tmp_data/error_board_all.txt'.format(EYEINHAND), error_board_all)
        np.savetxt('{}/weld_calib_sdk/tmp_data/error_base_all.txt'.format(EYEINHAND), error_base_all)
        print(np.hstack((error_base,np.var(error_list2base, axis=0, keepdims=True).squeeze().reshape(63,3))))
        
if __name__ == '__main__':
    a = auto_eye2tcp()
    # a.clear_folder(a.data_path)
    a.move_point([-250.911880493164,-97.13201904296875,447.5170593261718,-177.1136779785156,12.65798091888427,7.553834915161133])
    a.take_photo_and_save_data(index = 0)
    a.move_point([-306.928741455078,-148.6852416992187,413.7843627929687,-168.7870330810547,13.9370126724243,12.15764141082763])
    a.take_photo_and_save_data(index = 1)
    a.move_point([-297.9131469726562,2.55972409248352,398.1556701660156,166.2165069580078,13.15503978729248,11.90475559234619])
    a.take_photo_and_save_data(index = 2)
    a.move_point([-265.5235595703125,-93.0757369995117,392.471923828125,-175.9078826904297,20.15210723876953,9.17325496673584])
    a.take_photo_and_save_data(index = 3)
    a.move_point([-415.6813659667968,-99.0832061767578,498.9789733886718,-174.7282257080078,-6.393736362457275,13.159029006958])
    a.take_photo_and_save_data(index = 4)
    # a.move_point([-529.6224975585938,-437.390899658203,225.8129425048828,-171.011001586914,3.021464586257934,133.804443359375])
    # a.take_photo_and_save_data(index = 4)
    # a.move_point([-335.7194213867187,-412.6579284667968,66.60006713867188,-126.3293533325195,7.962363243103027,138.1767120361328])
    # a.take_photo_and_save_data(index = 5)
    a.initialize()
    
    
    
    # a.move_point([-689.8184858508737,
    #   73.80984831668859,
    #   436.62384714127603,
    #   -89.25816968693715,
    #   0.3212641536438313,
    #   87.15611423097765])
    # a.move_point([-504.482940673828, -471.2942810058593, 86.80835723876953, -162.4909515380859, 0.29752063751220703,
    #                138.2538909912109])
    # a.take_photo_and_save_data(index = 'tmp')
    # a.tcp2base_new()
    # a.execute()
    
    # a.error_analysis()
    # depth_img_path_tmp = '{}/tmp/pos.exr'.format(a.path)
    # gray_img_path_tmp = '{}/tmp/pos.bmp'.format(a.path)
    # board2cam_current_rmtxs, board2cam_current_tvecs, error, centers = Get_Board2Cam_Transform_3D(gray_img_path_tmp, depth_img_path_tmp, a.camera_mtx, a.camera_dist)
    # print(error)
    
    
    # tcp2base_rmtxs = []
    # tcp2base_tvecs = []
    # board2cam_rmtxs = []
    # board2cam_tvecs = []
    # data_path = '{}/cloud/pos'.format(a.path)
    # dx,dy,dz = 1,1,1
    # for i in range(2,5):
    #     print(i)
    #     folder = data_path + str(i)
    #     tcp2base_current = np.load(folder+"/matrix_tcp2base.npy")
    #     board2cam_current = np.load(folder+"/matrix_board2cam.npy")
    #     tcp2base_rmtxs.append(tcp2base_current[:3,:3])
    #     tcp2base_tvecs.append(tcp2base_current[:3,3]+np.array([dx,dy,dz]))
    #     board2cam_rmtxs.append(board2cam_current[:3,:3])
    #     board2cam_tvecs.append(board2cam_current[:3,3]+np.array([dx,dy,dz]))

    # cam2tcp_rmtx, cam2tcp_tvec = cv2.calibrateHandEye(tcp2base_rmtxs, tcp2base_tvecs, board2cam_rmtxs, board2cam_tvecs,
    #                                             method=cv2.CALIB_HAND_EYE_PARK)
    # print(cam2tcp_rmtx, cam2tcp_tvec)
    # cam2tcp_current = np.zeros((4,4))
    # cam2tcp_current[:3,:3] = cam2tcp_rmtx
    # cam2tcp_current[:3,3] = cam2tcp_tvec.reshape(3,)
    
    # for i in range(2,5):
    #     print(i)
    #     folder = data_path + str(i)
    #     tcp2base_current = np.load(folder+"/matrix_tcp2base.npy")
    #     board2cam_current = np.load(folder+"/matrix_board2cam.npy")
    #     board2base_current = tcp2base_current @ cam2tcp_current @ board2cam_current
    #     print(board2base_current[:3,-1])

    

    
        
        
