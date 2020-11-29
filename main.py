import os
import pathlib
from os import listdir, walk
from os.path import isfile, join

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QCheckBox, QListWidgetItem, QComboBox, QWidget, \
    QHBoxLayout, QLayout, QVBoxLayout, QStyleFactory, QLabel
from PyQt5 import QtCore,uic
import sys

form_class = uic.loadUiType("fcomp.ui")[0]  # Load the UI

class MyWindowClass(QMainWindow, form_class):
    isSearchBySize = False
    folderName = ''
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('File comparator')
        self.stopSearch.setVisible(False)


    def folderSearch_clicked(self):
        folderName = QFileDialog.getExistingDirectory(self,'Select a directory for search')
        if folderName:
            print(folderName)
            self.folderName.setText(folderName)
            self.folderName = folderName


    def stopSearch_clicked(self):
        pass

    def SearchBySize_clicked(self):
        self.isSearchBySize = self.SearchBySize.isChecked()
        print(self.isSearchBySize)


    def Compare_clicked(self):
        self.stopSearch.setVisible(True)

        print('Reading file list...')
        self.folderName = 'D:/Korovin/work/Education/python'
        # get list of files
        self.filenames = [(file.absolute(),os.path.getsize(file)) for file in pathlib.Path(self.folderName).glob('**/*')]
        # sort list of files by size
        self.filenames.sort(key=lambda x:x[1], reverse=True)


        print('Finding duplicates...')
        duplicates = {}
        for i,file in enumerate(self.filenames):
            if file[1] in duplicates.keys():
                duplicates[file[1]].append(i)
            else:
                duplicates[file[1]] = [i]

        # duplicated_files = {}
        for k in duplicates:
            if len(duplicates[k])>1:
                print(k, ':', duplicates[k])

                # search duplicates
                # if self.isSearchBySize:
                ind = duplicates[k]
                while len(ind)>1:
                    i1 = ind.pop(0)
                    duplicated_files = [[i1]]
                    n = 0
                    print('ind1 = ', ind)
                    print('len(ind) > n:',len(ind) > n)
                    while len(ind) > n:
                        print('self.filenames[i1][0], self.filenames[ind[n]][0]\n',self.filenames[i1][0], '\n',self.filenames[ind[n]][0])
                        if compare_two_files(self.filenames[i1][0], self.filenames[ind[n]][0]):
                            print('n = ', n)
                            i2 = ind.pop(n)
                            print('ind2 = ', ind)
                            duplicated_files[-1].append(i2)
                        else:
                            n += 1
                        print('ind3 = ', ind)
                print('\nduplicated_files = ', duplicated_files)


                for dups_ind in duplicated_files:
                    print('dups_ind = ', dups_ind)

                    if len(dups_ind)>1:
                        print('len(dups_ind) = ', len(dups_ind))
                        self.put_files_in_list(dups_ind,k)



    def put_files_in_list(self,dups_ind,f_size):
        self.stopSearch.setVisible(False)
        print('dups_ind = ', dups_ind)
        print('f_size = ', f_size)

        item = QListWidgetItem()
        widget = QWidget()
        widget_layout = QVBoxLayout()
        # add title
        label = QLabel()
        text = 'File size ' + str(f_size)  # label text
        widget_layout.addWidget(label)
        # add the list of the same files
        for i in dups_ind:
            checkBox = QCheckBox()
            checkBox.setText(str(self.filenames[i][0]))
            text += ' | ' + os.path.basename(self.filenames[i][0])
            widget_layout.addWidget(checkBox)
        label.setText(text)

        widget_layout.addStretch()
        # widget_layout.setSizeConstraint(QLayout.SetFixedSize)
        widget.setLayout(widget_layout)
        item.setSizeHint(widget.sizeHint())
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)

        # if the same names (text files)
        # import difflib
        # bin_1 = open("file1").read()
        # bin_2 = open("file2").read()
        # for line in difflib.context_diff(bin_1, bin_2):
        #     print(line)

def compare_two_files(name1, name2):
    with open(name1, "rb") as one:
        with open(name2, "rb") as two:
            chunk = other = True
            while chunk or other:
                chunk = one.read(1000)
                other = two.read(1000)
                if chunk != other:
                    return False
    return True

app = QApplication(sys.argv)
if 'Fusion' in QStyleFactory.keys():
    print('Fusion is found. Applying this style.')
    app.setStyle('Fusion')

myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()