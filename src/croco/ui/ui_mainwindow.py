# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\CroCo_qt.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(442, 227)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/data/images/python-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label3 = QtWidgets.QLabel(self.tab)
        self.label3.setObjectName("label3")
        self.gridLayout_2.addWidget(self.label3, 0, 0, 1, 2)
        self.convert_input_dropdown = QtWidgets.QComboBox(self.tab)
        self.convert_input_dropdown.setObjectName("convert_input_dropdown")
        self.convert_input_dropdown.addItem("")
        self.convert_input_dropdown.addItem("")
        self.convert_input_dropdown.addItem("")
        self.gridLayout_2.addWidget(self.convert_input_dropdown, 0, 2, 1, 1)
        self.label4 = QtWidgets.QLabel(self.tab)
        self.label4.setObjectName("label4")
        self.gridLayout_2.addWidget(self.label4, 0, 3, 1, 1)
        self.convert_output_dropdown = QtWidgets.QComboBox(self.tab)
        self.convert_output_dropdown.setObjectName("convert_output_dropdown")
        self.convert_output_dropdown.addItem("")
        self.gridLayout_2.addWidget(self.convert_output_dropdown, 0, 4, 1, 2)
        self.convert_load_btn = QtWidgets.QPushButton(self.tab)
        self.convert_load_btn.setObjectName("convert_load_btn")
        self.gridLayout_2.addWidget(self.convert_load_btn, 1, 2, 1, 1)
        self.convert_output_btn = QtWidgets.QPushButton(self.tab)
        self.convert_output_btn.setObjectName("convert_output_btn")
        self.gridLayout_2.addWidget(self.convert_output_btn, 1, 4, 1, 2)
        self.label1 = QtWidgets.QLabel(self.tab)
        self.label1.setObjectName("label1")
        self.gridLayout_2.addWidget(self.label1, 2, 0, 1, 1)
        self.label2 = QtWidgets.QLabel(self.tab)
        self.label2.setObjectName("label2")
        self.gridLayout_2.addWidget(self.label2, 2, 3, 1, 2)
        self.convert_quit = QtWidgets.QPushButton(self.tab)
        self.convert_quit.setObjectName("convert_quit")
        self.gridLayout_2.addWidget(self.convert_quit, 4, 4, 1, 2)
        self.convert_start = QtWidgets.QPushButton(self.tab)
        self.convert_start.setObjectName("convert_start")
        self.gridLayout_2.addWidget(self.convert_start, 4, 0, 1, 1)
        self.convert_input_lbl = QtWidgets.QLabel(self.tab)
        self.convert_input_lbl.setText("")
        self.convert_input_lbl.setObjectName("convert_input_lbl")
        self.gridLayout_2.addWidget(self.convert_input_lbl, 3, 0, 1, 3)
        self.convert_output_lbl = QtWidgets.QLabel(self.tab)
        self.convert_output_lbl.setText("")
        self.convert_output_lbl.setObjectName("convert_output_lbl")
        self.gridLayout_2.addWidget(self.convert_output_lbl, 3, 3, 1, 3)
        self.label1.raise_()
        self.convert_quit.raise_()
        self.label4.raise_()
        self.convert_load_btn.raise_()
        self.convert_output_btn.raise_()
        self.label3.raise_()
        self.label2.raise_()
        self.convert_input_dropdown.raise_()
        self.convert_output_dropdown.raise_()
        self.convert_start.raise_()
        self.convert_input_lbl.raise_()
        self.convert_output_lbl.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.assign_load_xlink_btn = QtWidgets.QPushButton(self.tab_2)
        self.assign_load_xlink_btn.setObjectName("assign_load_xlink_btn")
        self.gridLayout.addWidget(self.assign_load_xlink_btn, 1, 0, 1, 1)
        self.assign_load_mgf_btn = QtWidgets.QPushButton(self.tab_2)
        self.assign_load_mgf_btn.setObjectName("assign_load_mgf_btn")
        self.gridLayout.addWidget(self.assign_load_mgf_btn, 1, 1, 1, 1)
        self.assign_output_btn = QtWidgets.QPushButton(self.tab_2)
        self.assign_output_btn.setObjectName("assign_output_btn")
        self.gridLayout.addWidget(self.assign_output_btn, 1, 2, 1, 1)
        self.assign_start_btn = QtWidgets.QPushButton(self.tab_2)
        self.assign_start_btn.setObjectName("assign_start_btn")
        self.gridLayout.addWidget(self.assign_start_btn, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)
        self.assign_xlink_lbl = QtWidgets.QLabel(self.tab_2)
        self.assign_xlink_lbl.setText("")
        self.assign_xlink_lbl.setObjectName("assign_xlink_lbl")
        self.gridLayout.addWidget(self.assign_xlink_lbl, 3, 0, 1, 1)
        self.assign_mgf_lbl = QtWidgets.QLabel(self.tab_2)
        self.assign_mgf_lbl.setText("")
        self.assign_mgf_lbl.setObjectName("assign_mgf_lbl")
        self.gridLayout.addWidget(self.assign_mgf_lbl, 3, 1, 1, 1)
        self.assign_outdir_lbl = QtWidgets.QLabel(self.tab_2)
        self.assign_outdir_lbl.setText("")
        self.assign_outdir_lbl.setObjectName("assign_outdir_lbl")
        self.gridLayout.addWidget(self.assign_outdir_lbl, 3, 2, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 442, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setMenuRole(QtWidgets.QAction.QuitRole)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setMenuRole(QtWidgets.QAction.AboutRole)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "The CroCo Cross-Link Converter"))
        self.label3.setText(_translate("MainWindow", "Input file format:"))
        self.convert_input_dropdown.setStatusTip(_translate("MainWindow", "Format for file input"))
        self.convert_input_dropdown.setItemText(0, _translate("MainWindow", "pLink"))
        self.convert_input_dropdown.setItemText(1, _translate("MainWindow", "Kojak"))
        self.convert_input_dropdown.setItemText(2, _translate("MainWindow", "xTable"))
        self.label4.setText(_translate("MainWindow", "Output File Format"))
        self.convert_output_dropdown.setStatusTip(_translate("MainWindow", "Format to convert file to"))
        self.convert_output_dropdown.setItemText(0, _translate("MainWindow", "xTable"))
        self.convert_load_btn.setText(_translate("MainWindow", "Load file(s)"))
        self.convert_output_btn.setText(_translate("MainWindow", "Output Dir"))
        self.label1.setText(_translate("MainWindow", "Reading From:"))
        self.label2.setText(_translate("MainWindow", "Writing To:"))
        self.convert_quit.setText(_translate("MainWindow", "Quit"))
        self.convert_start.setStatusTip(_translate("MainWindow", "Start the conversion"))
        self.convert_start.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Conversion"))
        self.assign_load_xlink_btn.setText(_translate("MainWindow", "Load xlink"))
        self.assign_load_mgf_btn.setText(_translate("MainWindow", "Load MGF"))
        self.assign_output_btn.setText(_translate("MainWindow", "Output Dir"))
        self.assign_start_btn.setText(_translate("MainWindow", "Start assignment"))
        self.label.setText(_translate("MainWindow", "xlink dir:"))
        self.label_2.setText(_translate("MainWindow", "MGF dir:"))
        self.label_3.setText(_translate("MainWindow", "output dir:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Assignment"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setStatusTip(_translate("MainWindow", "Exit the programme"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("MainWindow", "About CroCo"))
        self.actionAbout.setStatusTip(_translate("MainWindow", "About CroCo"))

import croco.ui.croco_rc
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
