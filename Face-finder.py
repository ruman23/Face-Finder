# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FaceFinder.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import glob
import subprocess
import re
import shutil
import datetime
import time
import re, string
import string
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
##############
    def selectFunction(self):
        print("select check")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            folderLocation=filenames[0]
            print(folderLocation)

            print('*******get the all image file from selected folder********')
            print(folderLocation)
            l1=glob.glob(folderLocation+"/*.jpg")
            l2=glob.glob(folderLocation+"/*.JPG")
            l3=glob.glob(folderLocation+"/*.png")
            l4=glob.glob(folderLocation+"/*.PNG")
            l5=glob.glob(folderLocation+"/*.jpeg")
            l6=glob.glob(folderLocation+"/*.JPEG")
            allFileName=l1+l2+l3+l4+l5+l6
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(allFileName)
            #print(allFileName)
            length= len(allFileName)-1
#           print(length)
#######################saving folder###########################   
            listValue = self.listWidget.currentItem().text()
            listValue = listValue.strip('\n')
            print(listValue)
            listValue= listValue.replace(" ","-") 
                
            #ts = time.time()
            #st = datetime.datetime.fromtimestamp(ts).strftime('-time-%H-%M-%S-date-%d-%m-%Y')
            savingLocation="/home/spectator/Pictures/"+listValue
            os.system('mkdir -p '+savingLocation)
            print("saving:"+savingLocation)
            slideValue=self.horizontalSlider.value()
            print(slideValue)
#########################saving folder####################################
            while length>=0:
                location=''.join(allFileName[length])
                print('orginal file name:'+location)
                str= './demos/classifier.py infer ./generated-embeddings/classifier.pkl '+''.join(allFileName[length])
                print(str)
                Input=subprocess.getoutput(str)
                #print(Input)
                print('#############accuracy and file##################')
                name = re.search('Predict (.+?) with', Input)
                if name:
                    name = name.group(1)
                accuracy = re.search('with (.+?) confidence', Input)
                if accuracy:
                    accuracy = accuracy.group(1)    

                print('name and accuracy:')
                print(name)
                print(accuracy)
                #print(slideValue)
#################################
                try:
                    accuracy=int(float(accuracy)*100)
                     
                    print(accuracy)
                    if listValue==name and accuracy>slideValue:
                        print("Got the correct person:"+listValue)
                        os.system('cp -a'+' '+location+' '+savingLocation)
                except:
                    print("this photo cannot be process") 
#############################################  
                #os.system(str)
                length=length-1
            #open('/home/spectator/Pictures/Face Finder')
            subprocess.getoutput('nautilus '+savingLocation)
            #######################




#####################  traning part  ###########################
    def processFunction(self):
########## fil e###########
        lineEditValue= self.lineEdit.text()
        lineEditValue = re.sub('[%s]' % re.escape(string.punctuation), '', lineEditValue)
        print("check line edit"+lineEditValue)
        lineEditValueForList=lineEditValue
        lineEditValue= lineEditValue.replace(" ","-")
        if len(lineEditValue)>0 :
            if os.path.isdir("/home/spectator/openface/training-images/"+lineEditValue):
                print("exist this path")
                w = QWidget()
                QMessageBox.information(w, "Message", "This name is already listed!!!\n Please type another name and try again.")
            else:
                
                w = QWidget()
                QMessageBox.information(w, "Guide", "Select a image from a folder.\n Which conatained 15 to 20 images of a single person.")
                dlg = QFileDialog()
                dlg.setFileMode(QFileDialog.DirectoryOnly)
                if dlg.exec_():
                    filenames = dlg.selectedFiles()
                    folderLocation=filenames[0]
                    print(folderLocation)
                    print("?????????????????????"+folderLocation)
                      
                    os.system('mkdir -p /home/spectator/openface/training-images/'+lineEditValue)
#                    #####copy image from folderLocation to 'mkdir -p /home/spectator/openface/training-images/'+lineEditValue #
#                    files = glob.iglob(os.path.join(folderLocation, "*.jpg | *.txt "))
#                    for file in files:
#                        if os.path.isfile(file):
#                            shutil.copy2(file, '/home/spectator/openface/training-images/'+lineEditValue)
                    tr='cp -a '+folderLocation+'/'+'*.jpg'+' '+'/home/spectator/openface/training-images/'+lineEditValue
                    os.system(tr)
                    tr='cp -a '+folderLocation+'/'+'*.jpeg'+' '+'/home/spectator/openface/training-images/'+lineEditValue
                    os.system(tr)
                    tr='cp -a '+folderLocation+'/'+'*.png'+' '+'/home/spectator/openface/training-images/'+lineEditValue
                    os.system(tr)
                    tr='cp -a '+folderLocation+'/'+'*.JPG'+' '+'/home/spectator/openface/training-images/'+lineEditValue
                    os.system(tr)
                    tr='cp -a '+folderLocation+'/'+'*.JPEG'+' '+'/home/spectator/openface/training-images/'+lineEditValue
                    os.system(tr)
                    tr='cp -a '+folderLocation+'/'+'*.PNG'+' '+'/home/spectator/openface/training-images/'+lineEditValue
                    os.system(tr)
                    
                    if os.path.exists('/home/spectator/openface/aligned-images/cache.t7'):
                        os.remove('/home/spectator/openface/aligned-images/cache.t7') 
                    os.system('./util/align-dlib.py ./training-images/ align outerEyesAndNose ./aligned-images/ --size 96')
                    os.system('./batch-represent/main.lua -outDir ./generated-embeddings/ -data ./aligned-images/')
                    os.system('./demos/classifier.py train ./generated-embeddings/')
                    ###########################
                    file = open("/home/spectator/openface/open-face-name-list.txt","a") 
                    file.write(lineEditValueForList+"\n") 
                    file.close() 

                    f=open("/home/spectator/openface/open-face-name-list.txt","r") 
                    line=f.readlines()
                    self.listWidget.addItems([line[-1]])
                     
                    w = QWidget()
                    QMessageBox.information(w, "Notification", "Successfully added to the list")
        else: 
            w = QWidget()
            QMessageBox.information(w, "Warning", "Empty name is not acceptable!!!\nPlease type a name.")
         
#################
       
        print("submit check")
       
        listValue = self.listWidget.currentItem().text()
        print(listValue)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('-time-%H-%M-%S-date-%d-%m-%Y')
        st=str(st)
        st='date and time'+st
        print(st)

  

        #os.system("./demos/classifier.py infer ./generated-embeddings/classifier.pkl SRK/srk1.jpg")
             #######################
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(580, 460)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(_fromUtf8("background-color:rgb(255, 255, 255);"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 80, 561, 281))
        self.listWidget.setStyleSheet(_fromUtf8("font: 15pt \"URW Bookman L\";\n"
"background-color:rgb(255, 249, 183);\n"
"color: rgb(0, 0, 0);"))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
#########################################################
        f=open("/home/spectator/openface/open-face-name-list.txt","r") 
        line=f.readlines()
        self.listWidget.addItems(line)
        
        #with open("/home/spectator/openface/open-face-name-list.txt","r") as f:
         #   lines = f.read().splitlines()
          #  last_line = str(lines[-1])
           # self.listWidget.addItems([last_line])
            #print (last_line)  
########################################################
        self.processButton = QtGui.QPushButton(self.centralwidget)
        self.processButton.setGeometry(QtCore.QRect(400, 10, 161, 27))
        self.processButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.processButton.setMouseTracking(False)
        self.processButton.setStyleSheet(_fromUtf8("font: 15pt \"URW Bookman L\";\n"
"background-color:rgb(255, 121, 77);\n"
"color: rgb(0, 0, 0);\n"
))
        self.processButton.setObjectName(_fromUtf8("processButton"))
        ####### add event###########
        self.processButton.clicked.connect(self.processFunction)
	######## #############################################
        self.selcetButton = QtGui.QPushButton(self.centralwidget)
        self.selcetButton.setGeometry(QtCore.QRect(10, 410, 150, 27))
        self.selcetButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.selcetButton.setStyleSheet(_fromUtf8("font: 15pt \"URW Bookman L\";\n"
"background-color:rgb(255, 121, 77);\n"
"color: rgb(0, 0, 0);\n"
))
        self.selcetButton.setObjectName(_fromUtf8("selcetButton"))
        ####### add event###########
        self.selcetButton.clicked.connect(self.selectFunction)
	######## #############################################
        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(170, 370, 391, 41))
        self.horizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.horizontalSlider.setAutoFillBackground(False)
        self.horizontalSlider.setMinimum(30)
        self.horizontalSlider.setPageStep(5)
        self.horizontalSlider.setProperty("value", 50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.horizontalSlider.setTickInterval(5)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 370, 151, 31))
        self.label_3.setStyleSheet(_fromUtf8("font: 15pt \"URW Bookman L\";\n"
"background-color:rgb(222, 226, 255);\n"
"color: rgb(0, 0, 0);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 381, 31))
        self.lineEdit.setStyleSheet(_fromUtf8("font: 15pt \"URW Bookman L\";\n"
"background-color:rgb(255, 249, 183);\n"
"color: rgb(0, 0, 0);"))
        self.lineEdit.setText(_fromUtf8(""))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 50, 261, 21))
        self.label.setStyleSheet(_fromUtf8("font: 15pt \"URW Bookman L\";\n"
"background-color:rgb(222, 226, 255);\n"
"color: rgb(0, 0, 0);"))
        self.label.setObjectName(_fromUtf8("label"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.processButton.setText(_translate("MainWindow", "Training Image", None))
        self.selcetButton.setText(_translate("MainWindow", "Target Image", None))
        self.label_3.setText(_translate("MainWindow", "Accuracy Level", None))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Type New Face Name", None))
        self.label.setText(_translate("MainWindow", "Select  a name to separate", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

