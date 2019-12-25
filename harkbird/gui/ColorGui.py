# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ColorGui.ui'
#
# Created: Tue Oct 10 14:31:06 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.ColorButtonBox = QtGui.QDialogButtonBox(Dialog)
        self.ColorButtonBox.setGeometry(QtCore.QRect(50, 560, 341, 32))
        self.ColorButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ColorButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.ColorButtonBox.setObjectName("ColorButtonBox")
        self.ColorTable = QtGui.QTableWidget(Dialog)
        self.ColorTable.setGeometry(QtCore.QRect(10, 10, 381, 541))
        self.ColorTable.setAutoScroll(False)
        self.ColorTable.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.ColorTable.setColumnCount(2)
        self.ColorTable.setObjectName("ColorTable")
        self.ColorTable.setColumnCount(2)
        self.ColorTable.setRowCount(0)
        self.ColorTable.horizontalHeader().setVisible(True)
        self.ColorTable.horizontalHeader().setHighlightSections(True)
        self.ColorTable.horizontalHeader().setStretchLastSection(True)
        self.ColorTable.verticalHeader().setVisible(False)
        self.ColorTable.verticalHeader().setHighlightSections(False)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.ColorButtonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.ColorButtonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Color", None, QtGui.QApplication.UnicodeUTF8))

