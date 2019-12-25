# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DivideGui.ui'
#
# Created: Tue Oct 17 11:10:27 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 100)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.DivideButtonBox = QtGui.QDialogButtonBox(Dialog)
        self.DivideButtonBox.setGeometry(QtCore.QRect(130, 60, 161, 32))
        self.DivideButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.DivideButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.DivideButtonBox.setObjectName("DivideButtonBox")
        self.DivideComboBox = QtGui.QComboBox(Dialog)
        self.DivideComboBox.setGeometry(QtCore.QRect(220, 30, 69, 22))
        self.DivideComboBox.setObjectName("DivideComboBox")
        self.DivideComboBox.addItem("")
        self.DivideComboBox.addItem("")
        self.DivideLineEdit = QtGui.QLineEdit(Dialog)
        self.DivideLineEdit.setGeometry(QtCore.QRect(10, 30, 201, 20))
        self.DivideLineEdit.setInputMask("")
        self.DivideLineEdit.setObjectName("DivideLineEdit")
        self.DivideLabel = QtGui.QLabel(Dialog)
        self.DivideLabel.setGeometry(QtCore.QRect(10, 10, 181, 20))
        self.DivideLabel.setObjectName("DivideLabel")

        self.retranslateUi(Dialog)
        self.DivideComboBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.DivideButtonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.DivideButtonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Input dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.DivideComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "seconds", None, QtGui.QApplication.UnicodeUTF8))
        self.DivideComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "pieces", None, QtGui.QApplication.UnicodeUTF8))
        self.DivideLabel.setText(QtGui.QApplication.translate("Dialog", "Please input the number of divide", None, QtGui.QApplication.UnicodeUTF8))

