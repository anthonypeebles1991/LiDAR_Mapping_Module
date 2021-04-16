# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plottingTool.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(438, 580)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setObjectName("browse_button")
        self.verticalLayout.addWidget(self.browse_button)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.filename_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filename_label.sizePolicy().hasHeightForWidth())
        self.filename_label.setSizePolicy(sizePolicy)
        self.filename_label.setObjectName("filename_label")
        self.horizontalLayout.addWidget(self.filename_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.plot_button = QtWidgets.QPushButton(self.centralwidget)
        self.plot_button.setEnabled(False)
        self.plot_button.setObjectName("plot_button")
        self.verticalLayout.addWidget(self.plot_button)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(101, 71))
        self.label_2.setMaximumSize(QtCore.QSize(101, 71))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/Images/LMMicon.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.info_box = QtWidgets.QTextEdit(self.groupBox)
        self.info_box.setEnabled(True)
        self.info_box.setMinimumSize(QtCore.QSize(400, 200))
        self.info_box.setReadOnly(True)
        self.info_box.setObjectName("info_box")
        self.gridLayout.addWidget(self.info_box, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.browse_button.setText(_translate("MainWindow", "Browse to LiDAR data file"))
        self.label.setText(_translate("MainWindow", "File Selected:"))
        self.filename_label.setText(_translate("MainWindow", "None"))
        self.plot_button.setText(_translate("MainWindow", "Plot"))
        self.groupBox.setTitle(_translate("MainWindow", "Info"))

import images
