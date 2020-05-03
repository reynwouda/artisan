#!/usr/bin/env python3

# ABOUT
# Artisan Cup Profile Dialog

# LICENSE
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later versison. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

# AUTHOR
# Marko Luther, 2020

from matplotlib import rcParams

from artisanlib.dialogs import ArtisanResizeablDialog
from artisanlib.widgets import MyQDoubleSpinBox

from PyQt5.QtCore import (Qt, pyqtSlot, QSettings)
from PyQt5.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QVBoxLayout, QLabel, 
                             QLineEdit,QPushButton, QComboBox, QDialogButtonBox, QHeaderView,
                             QTableWidget, QDoubleSpinBox, QGroupBox)

class flavorDlg(ArtisanResizeablDialog):
    def __init__(self, parent = None, aw = None):
        super(flavorDlg,self).__init__(parent, aw)
        self.setModal(True)
        rcParams['path.effects'] = []
        #avoid question mark context help
        flags = self.windowFlags()
        helpFlag = Qt.WindowContextHelpButtonHint
        flags = flags & (~helpFlag)
        self.setWindowFlags(flags)
        self.setWindowTitle(QApplication.translate("Form Caption","Cup Profile",None))
        
        settings = QSettings()
        if settings.contains("FlavorProperties"):
            self.restoreGeometry(settings.value("FlavorProperties"))
            
        defaultlabel = QLabel(QApplication.translate("Label","Default",None))
        self.defaultcombobox = QComboBox()
        self.defaultcombobox.addItems(["","Artisan","SCCA","CQI","SweetMarias","C","E","CoffeeGeek","Intelligentsia","IIAC","WCRC","*CUSTOM*"])
        self.defaultcombobox.setCurrentIndex(0)
        self.lastcomboboxIndex = 0
        self.defaultcombobox.currentIndexChanged.connect(self.setdefault)
        self.flavortable = QTableWidget()
        self.flavortable.setTabKeyNavigation(True)
        self.createFlavorTable()
        leftButton = QPushButton("<")
        leftButton.setFocusPolicy(Qt.NoFocus)
        leftButton.clicked.connect(self.moveLeft)
        rightButton = QPushButton(">")
        rightButton.setFocusPolicy(Qt.NoFocus)
        rightButton.clicked.connect(self.moveRight)
        addButton = QPushButton(QApplication.translate("Button","Add",None))
        addButton.setFocusPolicy(Qt.NoFocus)
        addButton.clicked.connect(self.addlabel)
        delButton = QPushButton(QApplication.translate("Button","Del",None))
        delButton.setFocusPolicy(Qt.NoFocus)
        delButton.clicked.connect(self.poplabel)
        saveImgButton = QPushButton(QApplication.translate("Button","Save Image",None))
        saveImgButton.setFocusPolicy(Qt.NoFocus)
        #saveImgButton.clicked.connect(self.aw.resizeImg_0_1) # save as PNG (raster)
        saveImgButton.clicked.connect(self.aw.saveVectorGraph_PDF) # save as PDF (vector)
        
        # connect the ArtisanDialog standard OK/Cancel buttons
        self.dialogbuttons.accepted.connect(self.close)
        self.dialogbuttons.removeButton(self.dialogbuttons.button(QDialogButtonBox.Cancel))
        
        self.backgroundCheck = QCheckBox(QApplication.translate("CheckBox","Background", None))
        if self.aw.qmc.flavorbackgroundflag:
            self.backgroundCheck.setChecked(True)
        self.backgroundCheck.clicked.connect(self.showbackground)
        aspectlabel = QLabel(QApplication.translate("Label","Aspect Ratio",None))
        self.aspectSpinBox = QDoubleSpinBox()
        self.aspectSpinBox.setToolTip(QApplication.translate("Tooltip","Aspect Ratio",None))
        self.aspectSpinBox.setRange(0.,2.)
        self.aspectSpinBox.setSingleStep(.1)
        self.aspectSpinBox.setValue(self.aw.qmc.flavoraspect)
        self.aspectSpinBox.valueChanged.connect(self.setaspect)
        flavorLayout = QHBoxLayout()
        flavorLayout.addWidget(self.flavortable)
        comboLayout = QHBoxLayout()
        comboLayout.addWidget(defaultlabel)
        comboLayout.addWidget(self.defaultcombobox)
        comboLayout.addStretch()
        aspectLayout = QHBoxLayout()
        aspectLayout.addWidget(self.backgroundCheck)
        aspectLayout.addWidget(aspectlabel)
        aspectLayout.addWidget(self.aspectSpinBox)
        aspectLayout.addStretch()
        blayout1 = QHBoxLayout()
        blayout1.addStretch()
        blayout1.addWidget(addButton)
        blayout1.addWidget(delButton)
        blayout1.addStretch()
        extralayout = QVBoxLayout()
        extralayout.addLayout(comboLayout)
        extralayout.addLayout(aspectLayout)
        extraGroupLayout = QGroupBox()
        extraGroupLayout.setLayout(extralayout)
        blayout = QHBoxLayout()
        blayout.addStretch()
        blayout.addWidget(leftButton)
        blayout.addWidget(rightButton)
        blayout.addStretch()
        mainButtonsLayout = QHBoxLayout()
        mainButtonsLayout.addWidget(saveImgButton)
        mainButtonsLayout.addStretch()
        mainButtonsLayout.addWidget(self.dialogbuttons)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(flavorLayout)
        mainLayout.addLayout(blayout1)
        mainLayout.addWidget(extraGroupLayout)
        mainLayout.addLayout(blayout)
#        mainLayout.addStretch()
        mainLayout.addLayout(mainButtonsLayout)
        self.setLayout(mainLayout)
        self.aw.qmc.flavorchart()
        self.dialogbuttons.button(QDialogButtonBox.Ok).setFocus()

    @pyqtSlot(float)
    def setaspect(self,_):
        self.aw.qmc.flavoraspect = self.aspectSpinBox.value()
        self.aw.qmc.flavorchart()

    def createFlavorTable(self):
        nflavors = len(self.aw.qmc.flavorlabels)
        
        # self.flavortable.clear() # this crashes Ubuntu 16.04
#        if ndata != 0:
#            self.flavortable.clearContents() # this crashes Ubuntu 16.04 if device table is empty and also sometimes else
        self.flavortable.clearSelection() # this seems to work also for Ubuntu 16.04
        
        if nflavors:
            self.flavortable.setRowCount(nflavors)
            self.flavortable.setColumnCount(3)
            self.flavortable.setHorizontalHeaderLabels([QApplication.translate("Table", "Label",None),
                                                        QApplication.translate("Table", "Value",None),
                                                        ""])
            self.flavortable.setAlternatingRowColors(True)
            self.flavortable.setEditTriggers(QTableWidget.NoEditTriggers)
            self.flavortable.setSelectionBehavior(QTableWidget.SelectRows)
            self.flavortable.setSelectionMode(QTableWidget.SingleSelection)
            self.flavortable.setShowGrid(True)
            #self.flavortable.verticalHeader().setSectionResizeMode(2)
            #populate table
            for i in range(nflavors):
                labeledit = QLineEdit(self.aw.qmc.flavorlabels[i])
                labeledit.textChanged.connect(self.setlabel)
                valueSpinBox = MyQDoubleSpinBox()
                valueSpinBox.setRange(0.,10.)
                valueSpinBox.setSingleStep(.25)
                valueSpinBox.setAlignment(Qt.AlignRight)
                val = self.aw.qmc.flavors[i]
                if self.aw.qmc.flavors[0] < 1. and self.aw.qmc.flavors[-1] < 1.: # < 0.5.0 version style compatibility
                    val *= 10.
                valueSpinBox.setValue(val)
                valueSpinBox.valueChanged.connect(self.setvalue)
                #add widgets to the table
                self.flavortable.setCellWidget(i,0,labeledit)
                self.flavortable.setCellWidget(i,1,valueSpinBox)
            self.flavortable.resizeColumnsToContents()
            header = self.flavortable.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)

    @pyqtSlot(bool)
    def showbackground(self,_):
        if self.backgroundCheck.isChecked():
            if not self.aw.qmc.background:
                message = QApplication.translate("Message","Background profile not found", None)
                self.aw.sendmessage(message)
                self.backgroundCheck.setChecked(False)
            else:
                if len(self.aw.qmc.backgroundFlavors) != len(self.aw.qmc.flavors):
                    message = QApplication.translate("Message","Background does not match number of labels", None)
                    self.aw.sendmessage(message)
                    self.aw.qmc.flavorbackgroundflag = False
                    self.backgroundCheck.setChecked(False)
                else:
                    self.aw.qmc.flavorbackgroundflag = True
                    self.aw.qmc.flavorchart()
        else:
            self.aw.qmc.flavorbackgroundflag = False
            self.aw.qmc.flavorchart()

    @pyqtSlot(bool)
    def moveLeft(self,_):
        self.aw.qmc.flavorstartangle += 5
        self.aw.qmc.flavorchart()
    
    @pyqtSlot(bool)
    def moveRight(self,_):
        self.aw.qmc.flavorstartangle -= 5
        self.aw.qmc.flavorchart()

    def savetable(self):
        for i in range(len(self.aw.qmc.flavorlabels)):
            labeledit = self.flavortable.cellWidget(i,0)
            valueSpinBox = self.flavortable.cellWidget(i,1)
            label = labeledit.text()
            if "\\n" in label:              #make multiple line text if "\n" found in label string
                parts = label.split("\\n")
                label = chr(10).join(parts)
            self.aw.qmc.flavorlabels[i] = label
            self.aw.qmc.flavors[i] = valueSpinBox.value()
        if self.lastcomboboxIndex == 10:
            # store the current labels as *CUSTOM*
            self.aw.qmc.customflavorlabels = self.aw.qmc.flavorlabels

    @pyqtSlot()
    @pyqtSlot("QString")
    def setlabel(self,_):
        x = self.aw.findWidgetsRow(self.flavortable,self.sender(),0)
        if x is not None:
            labeledit = self.flavortable.cellWidget(x,0)
            self.aw.qmc.flavorlabels[x] = labeledit.text()
            self.aw.qmc.updateFlavorchartLabel(x) # fast incremental redraw

    @pyqtSlot(float)
    def setvalue(self,_):
        x = self.aw.findWidgetsRow(self.flavortable,self.sender(),1)
        if x is not None:
            valueSpinBox = self.flavortable.cellWidget(x,1)
            self.aw.qmc.flavors[x] = valueSpinBox.value()
#            self.aw.qmc.flavorchart() # slow full redraw
            self.aw.qmc.updateFlavorchartValues() # fast incremental redraw

    @pyqtSlot(int)
    def setdefault(self,_):
        if self.lastcomboboxIndex == 10:
            # store the current labels as *CUSTOM*
            self.aw.qmc.customflavorlabels = self.aw.qmc.flavorlabels
        dindex =  self.defaultcombobox.currentIndex()
        #["","Artisan","SCCA","CQI","SweetMarias","C","E","coffeegeek","Intelligentsia","WCRC"]
        if dindex > 0 or dindex < 11:
            self.aw.qmc.flavorstartangle = 90
        if dindex == 1:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.artisanflavordefaultlabels)
        elif dindex == 2:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.SCCAflavordefaultlabels)
        elif dindex == 3:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.CQIflavordefaultlabels)
        elif dindex == 4:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.SweetMariasflavordefaultlabels)
        elif dindex == 5:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.Cflavordefaultlabels)
        elif dindex == 6:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.Eflavordefaultlabels)
        elif dindex == 7:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.coffeegeekflavordefaultlabels)
        elif dindex == 8:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.Intelligentsiaflavordefaultlabels)
        elif dindex == 9:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.IstitutoInternazionaleAssaggiatoriCaffe)
        elif dindex == 10:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.WorldCoffeeRoastingChampionship)
        elif dindex == 11:
            self.aw.qmc.flavorlabels = list(self.aw.qmc.customflavorlabels)
        else:
            return
        self.aw.qmc.flavors = [5.]*len(self.aw.qmc.flavorlabels)
        self.createFlavorTable()
        self.aw.qmc.flavorchart()
        self.lastcomboboxIndex = dindex

    @pyqtSlot(bool)
    def addlabel(self,_):
        self.aw.qmc.flavorlabels.append("???")
        self.aw.qmc.flavors.append(5.)
        self.createFlavorTable()
        self.aw.qmc.flavorchart()

    @pyqtSlot(bool)
    def poplabel(self):
        fn = len(self.aw.qmc.flavors)
        self.aw.qmc.flavors = self.aw.qmc.flavors[:(fn-1)]
        self.aw.qmc.flavorlabels = self.aw.qmc.flavorlabels[:(fn -1)]
        self.createFlavorTable()
        self.aw.qmc.flavorchart()

    def closeEvent(self,_):
        self.close()

    @pyqtSlot()
    def close(self):
        settings = QSettings()
        #save window geometry
        settings.setValue("FlavorProperties",self.saveGeometry())
        self.savetable()
        self.aw.qmc.fileDirty()
        if self.aw.qmc.ax1 is not None:
            try:
                self.aw.qmc.fig.delaxes(self.aw.qmc.ax1)
            except:
                pass
        self.aw.qmc.fig.clf()
        self.aw.qmc.clearFlavorChart()
        self.aw.redrawOnResize = True
        self.aw.qmc.redraw(recomputeAllDeltas=False)
        self.aw.showControls()
        self.accept()