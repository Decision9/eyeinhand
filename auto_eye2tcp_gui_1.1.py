import time
from shutil import copyfile
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QFileDialog, QMessageBox, QHeaderView, \
    QAbstractItemView, QTableWidgetItem, QStyledItemDelegate
from PyQt5.QtGui import QPixmap, QImage, QStandardItemModel, QStandardItem, QColor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
import sys
import os
from auto_eye2tcp import auto_eye2tcp


class ColorDelegate(QStyledItemDelegate):
    def __init__(self, row, parent=None):
        super(ColorDelegate, self).__init__(parent)
        self.row = row

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.row() == self.row:
            option.backgroundBrush = QColor(Qt.green)


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1105, 921)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")
        self.verticalLayout_5.addWidget(self.label_logo)
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 213, 196))
        self.page.setObjectName("page")
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 213, 196))
        self.page_2.setObjectName("page_2")
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 213, 253))
        self.page_3.setObjectName("page_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_3 = QtWidgets.QLabel(self.page_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_13.addWidget(self.label_3)
        self.spinBox_dot1 = QtWidgets.QSpinBox(self.page_3)
        self.spinBox_dot1.setObjectName("spinBox_dot1")
        self.horizontalLayout_13.addWidget(self.spinBox_dot1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_4 = QtWidgets.QLabel(self.page_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_14.addWidget(self.label_4)
        self.spinBox_dot2 = QtWidgets.QSpinBox(self.page_3)
        self.spinBox_dot2.setObjectName("spinBox_dot2")
        self.horizontalLayout_14.addWidget(self.spinBox_dot2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_5 = QtWidgets.QLabel(self.page_3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_15.addWidget(self.label_5)
        self.spinBox_dist1 = QtWidgets.QSpinBox(self.page_3)
        self.spinBox_dist1.setObjectName("spinBox_dist1")
        self.horizontalLayout_15.addWidget(self.spinBox_dist1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_6 = QtWidgets.QLabel(self.page_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_17.addWidget(self.label_6)
        self.spinBox_dist2 = QtWidgets.QSpinBox(self.page_3)
        self.spinBox_dist2.setObjectName("spinBox_dist2")
        self.horizontalLayout_17.addWidget(self.spinBox_dist2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_17)
        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 1)
        self.verticalLayout_7.setStretch(2, 1)
        self.verticalLayout_7.setStretch(3, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout_7)
        self.toolBox.addItem(self.page_3, "")
        self.verticalLayout_5.addWidget(self.toolBox)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_5.addWidget(self.textBrowser)
        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 2)
        self.verticalLayout_5.setStretch(2, 2)
        self.horizontalLayout_19.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.horizontalLayout_12.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_x = QtWidgets.QLabel(self.centralwidget)
        self.label_x.setObjectName("label_x")
        self.horizontalLayout_3.addWidget(self.label_x)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setDecimals(4)
        self.doubleSpinBox.setMinimum(-999.99)
        self.doubleSpinBox.setMaximum(999.99)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_3.addWidget(self.doubleSpinBox)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_y = QtWidgets.QLabel(self.centralwidget)
        self.label_y.setObjectName("label_y")
        self.horizontalLayout_4.addWidget(self.label_y)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2.setDecimals(4)
        self.doubleSpinBox_2.setMinimum(-999.99)
        self.doubleSpinBox_2.setMaximum(999.99)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.horizontalLayout_4.addWidget(self.doubleSpinBox_2)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_z = QtWidgets.QLabel(self.centralwidget)
        self.label_z.setObjectName("label_z")
        self.horizontalLayout_5.addWidget(self.label_z)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_3.setDecimals(4)
        self.doubleSpinBox_3.setMinimum(-999.99)
        self.doubleSpinBox_3.setMaximum(999.99)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.horizontalLayout_5.addWidget(self.doubleSpinBox_3)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_dx = QtWidgets.QLabel(self.centralwidget)
        self.label_dx.setObjectName("label_dx")
        self.horizontalLayout_6.addWidget(self.label_dx)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_4.setDecimals(4)
        self.doubleSpinBox_4.setMinimum(-999.99)
        self.doubleSpinBox_4.setMaximum(999.99)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        self.horizontalLayout_6.addWidget(self.doubleSpinBox_4)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_dy = QtWidgets.QLabel(self.centralwidget)
        self.label_dy.setObjectName("label_dy")
        self.horizontalLayout_8.addWidget(self.label_dy)
        self.doubleSpinBox_5 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_5.setDecimals(4)
        self.doubleSpinBox_5.setMinimum(-999.99)
        self.doubleSpinBox_5.setMaximum(999.99)
        self.doubleSpinBox_5.setObjectName("doubleSpinBox_5")
        self.horizontalLayout_8.addWidget(self.doubleSpinBox_5)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_dz = QtWidgets.QLabel(self.centralwidget)
        self.label_dz.setObjectName("label_dz")
        self.horizontalLayout_7.addWidget(self.label_dz)
        self.doubleSpinBox_6 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_6.setDecimals(4)
        self.doubleSpinBox_6.setMinimum(-999.99)
        self.doubleSpinBox_6.setMaximum(999.99)
        self.doubleSpinBox_6.setObjectName("doubleSpinBox_6")
        self.horizontalLayout_7.addWidget(self.doubleSpinBox_6)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12.addLayout(self.verticalLayout)
        self.nowphoto_Button = QtWidgets.QPushButton(self.centralwidget)
        self.nowphoto_Button.setObjectName("nowphoto_Button")
        self.horizontalLayout_12.addWidget(self.nowphoto_Button)
        self.horizontalLayout_12.setStretch(0, 1)
        self.horizontalLayout_12.setStretch(1, 5)
        self.horizontalLayout_12.setStretch(2, 1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_12)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_var = QtWidgets.QLabel(self.tab)
        self.label_var.setObjectName("label_var")
        self.verticalLayout_8.addWidget(self.label_var)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.photo_label = QtWidgets.QLabel(self.tab)
        #self.photo_label.setTextFormat(QtCore.Qt.MarkdownText)
        self.photo_label.setObjectName("photo_label")
        self.horizontalLayout_18.addWidget(self.photo_label)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tableView_pos = QtWidgets.QTableView(self.tab)
        self.tableView_pos.setObjectName("tableView_pos")
        self.verticalLayout_4.addWidget(self.tableView_pos)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.verticalLayout_4.setStretch(0, 3)
        self.verticalLayout_4.setStretch(1, 1)
        self.horizontalLayout_18.addLayout(self.verticalLayout_4)
        self.horizontalLayout_18.setStretch(0, 5)
        self.horizontalLayout_18.setStretch(1, 1)
        self.verticalLayout_8.addLayout(self.horizontalLayout_18)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.spinBox_pose = QtWidgets.QSpinBox(self.tab)
        self.spinBox_pose.setObjectName("spinBox_pose")
        self.horizontalLayout_2.addWidget(self.spinBox_pose)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.takephoto_Button = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.takephoto_Button.sizePolicy().hasHeightForWidth())
        self.takephoto_Button.setSizePolicy(sizePolicy)
        self.takephoto_Button.setObjectName("takephoto_Button")
        self.horizontalLayout.addWidget(self.takephoto_Button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.Initialize_Button = QtWidgets.QPushButton(self.tab)
        self.Initialize_Button.setObjectName("Initialize_Button")
        self.horizontalLayout.addWidget(self.Initialize_Button)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_eye2tcp = QtWidgets.QPushButton(self.tab)
        self.pushButton_eye2tcp.setObjectName("pushButton_eye2tcp")
        self.horizontalLayout.addWidget(self.pushButton_eye2tcp)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.verticalLayout_8.setStretch(1, 10)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_new_var = QtWidgets.QLabel(self.tab_2)
        self.label_new_var.setObjectName("label_new_var")
        self.verticalLayout_9.addWidget(self.label_new_var)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.photo_label_2 = QtWidgets.QLabel(self.tab_2)
        #Sself.photo_label_2.setTextFormat(QtCore.Qt.MarkdownText)
        self.photo_label_2.setObjectName("photo_label_2")
        self.horizontalLayout_20.addWidget(self.photo_label_2)
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_20.addWidget(self.label_8)
        self.horizontalLayout_20.setStretch(0, 1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.tmp_Button = QtWidgets.QPushButton(self.tab_2)
        self.tmp_Button.setObjectName("tmp_Button")
        self.horizontalLayout_10.addWidget(self.tmp_Button)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem5)
        self.execute_Button = QtWidgets.QPushButton(self.tab_2)
        self.execute_Button.setObjectName("execute_Button")
        self.horizontalLayout_10.addWidget(self.execute_Button)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem6)
        self.pushButton_eye2tcp_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_eye2tcp_2.setObjectName("pushButton_eye2tcp_2")
        self.horizontalLayout_10.addWidget(self.pushButton_eye2tcp_2)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.verticalLayout_9.addLayout(self.horizontalLayout_10)
        self.verticalLayout_9.setStretch(1, 5)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_6.addWidget(self.tabWidget)
        self.tableView_step = QtWidgets.QTableView(self.centralwidget)
        self.tableView_step.setObjectName("tableView_step")
        self.verticalLayout_6.addWidget(self.tableView_step)
        self.verticalLayout_6.setStretch(0, 2)
        self.verticalLayout_6.setStretch(2, 1)
        self.horizontalLayout_19.addLayout(self.verticalLayout_6)
        self.horizontalLayout_19.setStretch(0, 1)
        self.horizontalLayout_19.setStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "优复博智能手眼标定软件(YOFO-IHECS)"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "相机设置"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "机械臂设置"))
        self.label_3.setText(_translate("MainWindow", "横向圆数："))
        self.label_4.setText(_translate("MainWindow", "纵向圆数："))
        self.label_5.setText(_translate("MainWindow", "横向间距："))
        self.label_6.setText(_translate("MainWindow", "纵向间距："))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("MainWindow", "标定设置"))
        self.label.setText(_translate("MainWindow", "TCP位姿："))
        self.label_x.setText(_translate("MainWindow", "x："))
        self.label_y.setText(_translate("MainWindow", "y："))
        self.label_z.setText(_translate("MainWindow", "z："))
        self.label_dx.setText(_translate("MainWindow", "rx："))
        self.label_dy.setText(_translate("MainWindow", "ry："))
        self.label_dz.setText(_translate("MainWindow", "rz："))
        self.nowphoto_Button.setText(_translate("MainWindow", "获取当前位姿"))
        self.label_var.setText(_translate("MainWindow", "标定误差值："))
        self.photo_label.setText(_translate("MainWindow", "照片显示区域"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:7pt;\">操作说明及注意事项</span></p><p><span style=\" font-size:7pt;\">1.流程为设定pos-移动机械臂-获取当前</span></p><p><span style=\" font-size:7pt;\">位姿-拍照-初始化标定-导出结果</span></p><p><span style=\" font-size:7pt;\">2.当前机械臂、相机、标定板初次标定请</span></p><p><span style=\" font-size:7pt;\">选择初始化标定</span></p><p><span style=\" font-size:7pt;\">3.右侧的表格中状态代表不同位姿下拍照</span></p><p><span style=\" font-size:7pt;\">是否可以使用，误差可以查看不同位姿下</span></p><p><span style=\" font-size:7pt;\">的误差</span></p><p><span style=\" font-size:7pt;\">4.通过右侧表格或下方pos设置几个位姿</span></p><p><span style=\" font-size:7pt;\">并拍照，拍照请先点击获取当前位姿</span></p><p><span style=\" font-size:7pt;\">5.至少需要三张照片才可以使用初始化</span></p><p><span style=\" font-size:7pt;\">标定，可以从右侧表格确认有效拍照位</span></p><p><span style=\" font-size:7pt;\">姿个数</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "pos:"))
        self.takephoto_Button.setText(_translate("MainWindow", "拍照"))
        self.Initialize_Button.setText(_translate("MainWindow", "初始化标定"))
        self.pushButton_eye2tcp.setText(_translate("MainWindow", "导出初始标定结果"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "初始化标定"))
        self.label_new_var.setText(_translate("MainWindow", "当前位姿拍照误差："))
        self.photo_label_2.setText(_translate("MainWindow", "照片显示区域"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:7pt;\">操作说明及注意事项</span></p><p><span style=\" font-size:7pt;\">1.流程为拍摄TMP照片-自动拍照计算结果</span></p><p><span style=\" font-size:7pt;\">-导出标定结果</span></p><p><span style=\" font-size:7pt;\">2.当前机械臂、相机和标定版如果未初始</span></p><p><span style=\" font-size:7pt;\">化标定，请勿使用重复标定</span></p><p><span style=\" font-size:7pt;\">3.重复标定的流程是先拍摄一张tmp照片，</span></p><p><span style=\" font-size:7pt;\">改位姿拍摄能够识别到标定版之后才能使</span></p><p><span style=\" font-size:7pt;\">用自动拍照</span></p><p><span style=\" font-size:7pt;\">4.自动拍照时机械臂会移动到不同位姿进</span></p><p><span style=\" font-size:7pt;\">行拍照，请等待一段时间，拍照结束可以</span></p><p><span style=\" font-size:7pt;\">导出标定结果文件保存。</span></p></body></html>"))
        self.tmp_Button.setText(_translate("MainWindow", "拍摄tmp照片"))
        self.execute_Button.setText(_translate("MainWindow", "自动拍照并计算结果"))
        self.pushButton_eye2tcp_2.setText(_translate("MainWindow", "导出结果"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "重复标定"))








        self.model_pos = QStandardItemModel(0 ,3)
        self.model_pos.setHorizontalHeaderLabels(['pos', '状态', '误差'])
        self.tableView_pos.setModel(self.model_pos)
        self.tableView_pos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_pos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_pos.setSelectionBehavior(QAbstractItemView.SelectRows)
        newItem = QTableWidgetItem("松鼠")
        newItem.setBackground(QColor(120, 130, 150))
        for i in range(6):
            self.model_pos.appendRow([
                        QStandardItem('%s' % str(i)),
                        QStandardItem('%s' % "未拍照"),
                        QStandardItem('%s' % "--"),
                    ])
        self.model_step = QStandardItemModel(0, 3)
        self.model_step.setHorizontalHeaderLabels(['时间', '输出信息', '状态'])
        self.tableView_step.setModel(self.model_step)
        self.tableView_step.setColumnWidth(0, 200)
        self.tableView_step.setColumnWidth(1, 1000)
        self.tableView_step.setColumnWidth(2, 200)
        self.tableView_step.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.pushButton_eye2tcp.clicked.connect(self.handle_pushButton_eye2tcp)
        self.pushButton_eye2tcp_2.clicked.connect(self.handle_pushButton_eye2tcp_2)
        self.tableView_pos.clicked.connect(self.on_comboBox_changed)
        self.data = {}
        self.takephoto_Button.clicked.connect(self.handle_camera_button)
        self.Initialize_Button.clicked.connect(self.handle_Initialize)
        self.nowphoto_Button.clicked.connect(self.handle_get_robot_xyz)
        self.execute_Button.clicked.connect(self.handle_execute_Button)
        self.tmp_Button.clicked.connect(self.handle_tmp_Button)
        self.directory_path = 'data/cloud'
        # 列出指定目录下的直接子文件夹
        sub_folders = [f for f in os.listdir(self.directory_path) if
                       os.path.isdir(os.path.join(self.directory_path, f))]
        self.right = 0
        #self.Initialize_Button.setEnabled(0)
        image = QPixmap("logo.png")
        image = image.scaled(self.label_logo.size()*5, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_logo.setPixmap(image)
        self.label_logo.setScaledContents(True)
        self.calib = auto_eye2tcp()

    def display_images(self):
        image = QPixmap(self.image_file)
        image = image.scaled(self.photo_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.photo_label.setPixmap(image)

    def display_images2(self):
        image = QPixmap("data/tmp/pos.bmp")
        image = image.scaled(self.photo_label_2.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.photo_label_2.setPixmap(image)

    def handle_get_robot_xyz(self):
        points = self.calib.get_robot_xyz()
        print(",".join(["{}".format(c) for c in points]))
        print(len(points))
        print(points)
        self.doubleSpinBox.setValue(round(points[0], 4))
        self.doubleSpinBox_2.setValue(round(points[1], 4))
        self.doubleSpinBox_3.setValue(round(points[2], 4))
        self.doubleSpinBox_4.setValue(round(points[3], 4))
        self.doubleSpinBox_5.setValue(round(points[4], 4))
        self.doubleSpinBox_6.setValue(round(points[5], 4))
        

    def handle_camera_button(self):
        if self.doubleSpinBox.value() == 0 or self.doubleSpinBox_2.value() == 0 or self.doubleSpinBox_3.value() == 0 or self.doubleSpinBox_4.value() == 0 or self.doubleSpinBox_5.value() == 0 or self.doubleSpinBox_6.value() == 0:
            print("请输入位姿值")
            self.list = []
            self.list.append(self.doubleSpinBox.value())
            self.list.append(self.doubleSpinBox_2.value())
            self.list.append(self.doubleSpinBox_3.value())
            self.list.append(self.doubleSpinBox_4.value())
            self.list.append(self.doubleSpinBox_5.value())
            self.list.append(self.doubleSpinBox_6.value())
            self.show_confirmation_dialog()

        else:
            self.list = []
            self.list.append(self.doubleSpinBox.value())
            self.list.append(self.doubleSpinBox_2.value())
            self.list.append(self.doubleSpinBox_3.value())
            self.list.append(self.doubleSpinBox_4.value())
            self.list.append(self.doubleSpinBox_5.value())
            self.list.append(self.doubleSpinBox_6.value())
            self.show_confirmation_dialog()
           

    def handle_tmp_Button(self):
        if self.doubleSpinBox.value() == 0 or self.doubleSpinBox_2.value() == 0 or self.doubleSpinBox_3.value() == 0 or self.doubleSpinBox_4.value() == 0 or self.doubleSpinBox_5.value() == 0 or self.doubleSpinBox_6.value() == 0:
            print("请输入位姿值")
        else:
            self.list = []
            self.list.append(self.doubleSpinBox.value())
            self.list.append(self.doubleSpinBox_2.value())
            self.list.append(self.doubleSpinBox_3.value())
            self.list.append(self.doubleSpinBox_4.value())
            self.list.append(self.doubleSpinBox_5.value())
            self.list.append(self.doubleSpinBox_6.value())
            self.show_confirmation_dialog2()



    def on_comboBox_changed(self,Item):
        try:
            self.pos_path = self.directory_path + "/" + "pos" + str(Item.row())
            self.image_file = self.pos_path + "/" + "pos" + str(Item.row()) + "_settled.bmp"
            self.point_file = self.pos_path + "/" + "point_information.txt"
            print(Item.row())
            self.spinBox_pose.setValue(Item.row())
            if os.path.exists(self.image_file):
                self.display_images()
            else:
                self.photo_label.clear()
            if os.path.exists(self.point_file):
                points = np.loadtxt(self.point_file)
                self.doubleSpinBox.setValue(round(points[0], 4))
                self.doubleSpinBox_2.setValue(round(points[1], 4))
                self.doubleSpinBox_3.setValue(round(points[2], 4))
                self.doubleSpinBox_4.setValue(round(points[3], 4))
                self.doubleSpinBox_5.setValue(round(points[4], 4))
                self.doubleSpinBox_6.setValue(round(points[5], 4))
        except Exception as e:
            print(e)

    def handle_Initialize(self):
        try:
            a,var = self.calib.initialize()
            self.label_var.setText(f"当前照片误差： {var}")
            self.model_step.appendRow([
                QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                QStandardItem('%s' % "初始化标定"),
                QStandardItem('%s' % "成功"),
            ])
            self.textBrowser.append(str(a))
        except Exception as e:
            print(e)

    def handle_execute_Button(self):
        self.calib.tcp2base_new()
        b,new_var=self.calib.execute()
        self.label_new_var.setText(f"当前照片误差： {new_var}")
        self.model_step.appendRow([
            QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
            QStandardItem('%s' % "自动拍照并计算结果"),
            QStandardItem('%s' % "成功"),
        ])
        self.textBrowser.append(str(b))

    def show_confirmation_dialog(self):
        try:
            # 创建一个确认对话框
            confirmation = QMessageBox()
            confirmation.setIcon(QMessageBox.Question)
            confirmation.setWindowTitle("确认对话框")
            my_string = ', '.join(map(str, self.list))
            confirmation.setText("位姿：" + my_string + ",请确认是否拍照")
            # 添加"确认"和"取消"按钮
            confirmation.addButton(QMessageBox.Yes)
            confirmation.addButton(QMessageBox.Cancel)
            # 显示对话框并等待用户响应
            result = confirmation.exec_()

            # 处理用户的响应
            if result == QMessageBox.Yes:
                self.calib.move_point(self.list)
                result,error=self.calib.take_photo_and_save_data(index=self.spinBox_pose.value())
                if result:
                    self.model_pos.setItem(self.spinBox_pose.value(), 1, QStandardItem("拍照成功"))
                    self.model_pos.setItem(self.spinBox_pose.value(), 2, QStandardItem(str(round(error, 4))))
                    self.model_step.appendRow([
                        QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                        QStandardItem('%s' % f"pos{self.spinBox_pose.value()}拍照"),
                        QStandardItem('%s' % "成功"),
                    ])
                    delegate = ColorDelegate(self.spinBox_pose.value(), self.tableView_pos)
                    self.tableView_pos.setItemDelegate(delegate)

                else:
                    self.model_step.appendRow([
                        QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                        QStandardItem('%s' % f"pos{self.spinBox_pose.value()}拍照"),
                        QStandardItem('%s' % "失败"),
                    ])
                    self.model_step.appendRow([
                        QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                        QStandardItem('%s' % error),
                        QStandardItem('%s' % "错误信息"),
                    ])
                
                self.right += 1
                if self.right == 3:
                    self.Initialize_Button.setEnabled(1)
                self.display_images()
            elif result == QMessageBox.Cancel:
                pass
        except Exception as e:
            print(e)

    def show_confirmation_dialog2(self):
        try:
            # 创建一个确认对话框
            confirmation = QMessageBox()
            confirmation.setIcon(QMessageBox.Question)
            confirmation.setWindowTitle("确认对话框")
            my_string = ', '.join(map(str, self.list))
            confirmation.setText("位姿：" + my_string + ",请确认是否拍照")

            # 添加"确认"和"取消"按钮
            confirmation.addButton(QMessageBox.Yes)
            confirmation.addButton(QMessageBox.Cancel)

            # 显示对话框并等待用户响应
            result = confirmation.exec_()

            # 处理用户的响应
            if result == QMessageBox.Yes:
                #self.calib.move_point(self.list)
                result,error=self.calib.take_photo_and_save_data(index = 'tmp')
                if result:
                    self.model_step.appendRow([
                        QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                        QStandardItem('%s' % f"tmp拍照"),
                        QStandardItem('%s' % "成功"),
                    ])
                    self.display_images2()
                    self.label_new_var.setText("当前位姿拍照误差："+str(error))
                else:
                    self.model_step.appendRow([
                        QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                        QStandardItem('%s' % f"tmp拍照"),
                        QStandardItem('%s' % "失败"),
                    ])
                    self.model_step.appendRow([
                        QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                        QStandardItem('%s' % error),
                        QStandardItem('%s' % "错误信息"),
                    ])
                    self.display_images2()
            elif result == QMessageBox.Cancel:
                pass
        except Exception as e:
            print(e)

    def handle_pushButton_eye2tcp(self):
        eye2tcp_path, _ = QFileDialog.getSaveFileName(self,"手眼标定文件", "./", "文本文件 (*.txt)")
        if eye2tcp_path:
            copyfile("data/matrix_cam2tcp.txt", eye2tcp_path)
            self.model_step.appendRow([
                QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                QStandardItem('%s' % "导出初始化标定结果"),
                QStandardItem('%s' % "成功"),
            ])
            self.textBrowser.append("已导出结果到文件")

    def handle_pushButton_eye2tcp_2(self):
        eye2tcp_path, _ = QFileDialog.getSaveFileName(self,"手眼标定文件", "./", "文本文件 (*.txt)")
        if eye2tcp_path:
            copyfile("data/matrix_cam2tcp_new.txt", eye2tcp_path)
            self.model_step.appendRow([
                QStandardItem('%s' % time.strftime('%H:%M:%S', time.localtime(time.time()))),
                QStandardItem('%s' % "导出自动标定结果"),
                QStandardItem('%s' % "成功"),
            ])
            self.textBrowser.append("已导出结果到文件")

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 实例化UI类
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowState(self.windowState() | QtCore.Qt.WindowMaximized)

if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
