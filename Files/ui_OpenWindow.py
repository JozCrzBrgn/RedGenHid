# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_OpenWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
        SplashScreen.resize(680, 400)
        self.centralwidget = QtWidgets.QWidget(SplashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("QFrame {\n"
"    background-color: rgb(35, 57, 91);\n"
"    color: rgb(38, 84, 38);\n"
"    border-radius: 20px;\n"
"}")
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setObjectName("dropShadowFrame")
        self.lbl_titulo = QtWidgets.QLabel(self.dropShadowFrame)
        self.lbl_titulo.setGeometry(QtCore.QRect(10, 59, 641, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(40)
        self.lbl_titulo.setFont(font)
        self.lbl_titulo.setStyleSheet("color: rgb(77, 168, 252)\n"
"/*color: rgb(81, 141, 181)*/")
        self.lbl_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.lbl_descripcion = QtWidgets.QLabel(self.dropShadowFrame)
        self.lbl_descripcion.setGeometry(QtCore.QRect(10, 130, 641, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.lbl_descripcion.setFont(font)
        self.lbl_descripcion.setStyleSheet("/*color: rgb(77, 168, 252)*/\n"
"color: rgb(81, 141, 181)")
        self.lbl_descripcion.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_descripcion.setObjectName("lbl_descripcion")
        self.progressBar = QtWidgets.QProgressBar(self.dropShadowFrame)
        self.progressBar.setGeometry(QtCore.QRect(30, 271, 591, 23))
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    \n"
"    background-color:rgb(201, 233, 252);/* rgb(239, 194, 15);*/\n"
"    color: rgb(0, 0, 0);\n"
"    border-style: none;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"    font: 75 14pt \"Times New Roman\";\n"
"}\n"
"\n"
"/*rgb(64, 157, 196) Fuerte*/\n"
"/*rgb(139, 211, 248) debil*/\n"
"QProgressBar::chunk{\n"
"    border-radius: 10px;    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.517, x2:0.96, y2:0.522727, stop:0.0113636 rgba(139, 211, 248, 255), stop:0.994318 rgba(64, 157, 196, 255));\n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.lbl_loading = QtWidgets.QLabel(self.dropShadowFrame)
        self.lbl_loading.setGeometry(QtCore.QRect(10, 298, 641, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.lbl_loading.setFont(font)
        self.lbl_loading.setStyleSheet("color:rgb(255, 255, 255);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.lbl_loading.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_loading.setObjectName("lbl_loading")
        self.lbl_creditos = QtWidgets.QLabel(self.dropShadowFrame)
        self.lbl_creditos.setGeometry(QtCore.QRect(320, 341, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_creditos.setFont(font)
        self.lbl_creditos.setStyleSheet("color:rgb(255, 255, 255)")
        self.lbl_creditos.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_creditos.setObjectName("lbl_creditos")
        self.verticalLayout.addWidget(self.dropShadowFrame)
        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "MainWindow"))
        self.lbl_titulo.setText(_translate("SplashScreen", "<html><head/><body><p><span style=\" font-weight:600;\">MY</span> APP NAME</p></body></html>"))
        self.lbl_descripcion.setText(_translate("SplashScreen", "<strong>APP</strong> DESCRIPTION"))
        self.lbl_loading.setText(_translate("SplashScreen", "Loading ..."))
        self.lbl_creditos.setText(_translate("SplashScreen", "<strong>Creado por:</strong> Josue Emmanuel Cruz Barragan"))
