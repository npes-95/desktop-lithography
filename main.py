import time
import sys

sys.path.append("lib/helper")
sys.path.append("lib/process")


from DMD import LightCrafter
from LEDs  import LED
from photomask import Photomask
from substrate import Substrate
from TinyG import MotorDriver
from CameraPreview import PiCameraPreview

from main_exposure import MainExposure
from test_exposure import TestExposure


from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QTabWidget, QVBoxLayout, QLineEdit, QFormLayout, QComboBox, QGroupBox, QFileDialog, QGridLayout, QLabel, QProgressBar, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = "Desktop Lithography Control Software - 1.0"
        self.left = 30
        self.top = 30
        self.width = 640
        self.height = 480
        #self.initInterfaces()
        self.initUI()
 
    def initUI(self):

        # basic window geometry
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # init tabs
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)


        self.show()
        
    def initInterfaces(self):
        
        self.dmd = LightCrafter()
        self.LED = LED()
        self.photomask = Photomask()
        self.substrate = Substrate()
        self.stage = MotorDriver()


class TableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # init camera preview 
        self.cameraPreview = PiCameraPreview()
 
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.launchTab = QWidget()   
        self.settingsTab = QWidget()
        self.previewTab = QWidget()
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.launchTab,"Launch")
        self.tabs.addTab(self.settingsTab,"Settings")
        self.tabs.addTab(self.previewTab,"Preview")
        

        # init first tab
        self.launchTab.layout = self.createLaunchTabLayout()
        self.launchTab.setLayout(self.launchTab.layout)

        # init second tab
        self.settingsTab.layout = self.createSettingsTabLayout()
        self.settingsTab.setLayout(self.settingsTab.layout)

        # init third tab
        self.previewTab.layout = self.createPreviewTabLayout()
        self.previewTab.setLayout(self.previewTab.layout)

 
        # Add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    # GUI SETUP

    def createLaunchTabLayout(self):
        
        # text box for console
        self.guiConsole = QTextEdit("Welcome to the Desktop Lithography Control GUI. Please check the settings and calibrate the substrate size before launching the operation. The etching parameters are taken directly from their fields when the operation is launched.")
        self.guiConsole.setReadOnly(True)

        # launch button 
        self.launchButton = QPushButton("Launch")
        self.launchButton.setToolTip("Launch photolithogrphy operation.")
        self.launchButton.clicked.connect(self.mainEtchLaunch)

        self.testButton = QPushButton("Test")
        self.testButton.setToolTip("Test photolithogrphy operation. Will print identical pattern at different exposure times.")
        self.testButton.clicked.connect(self.testEtchLaunch)
        
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setEnabled(False)
        self.cancelButton.clicked.connect(self.cancelProcess)
        
        self.launchButtonLayout = QHBoxLayout()
        self.launchButtonLayout.addWidget(self.launchButton)
        self.launchButtonLayout.addWidget(self.testButton)
        self.launchButtonLayout.addWidget(self.cancelButton)
        
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0,100)
        

        self.launchLayout = QVBoxLayout(self)
        self.launchLayout.addWidget(self.guiConsole)
        self.launchLayout.addLayout(self.launchButtonLayout)
        self.launchLayout.addWidget(self.progressBar)

        return self.launchLayout

    def createSettingsTabLayout(self):

        # init group boxes
        self.mainSettingGB = QGroupBox("Main")
        self.testSettingGB = QGroupBox("Test")


        # ~~~ MAIN SETTINGS ~~~

        # init main settings form layout
        self.mainFormLayout = QFormLayout() 

        # settings text entries
        self.exposureTimeTB = QLineEdit("2")
        self.interationsTB = QLineEdit("50")
        self.substrateDiameterTB = QLineEdit("100")
        

        # substrate type combo box
        self.substrateShapeCB = QComboBox()
        self.substrateShapeCB.addItem("Circle")
        self.substrateShapeCB.addItem("Rectangle")

        # button for browsing files, textbox for displaying selected file
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.openFileDialog)
        self.photomaskTB = QLineEdit()

        # file browser layout
        self.fileBrowserLayout = QHBoxLayout()
        self.fileBrowserLayout.addWidget(self.photomaskTB)
        self.fileBrowserLayout.addWidget(self.browseButton)



        # add elements to form layout
        self.mainFormLayout.addRow("Exposure time (s):", self.exposureTimeTB)
        self.mainFormLayout.addRow("Pattern iterations:", self.interationsTB)
        self.mainFormLayout.addRow("Substrate diameter:", self.substrateDiameterTB)
        self.mainFormLayout.addRow("Substrate shape:", self.substrateShapeCB)
        self.mainFormLayout.addRow("Photomask:", self.fileBrowserLayout)

        # set alignement to left
        self.mainFormLayout.setFormAlignment(Qt.AlignLeft)
        self.mainFormLayout.setLabelAlignment(Qt.AlignLeft)


        # ~~~ TEST SETTINGS ~~~~

        # add form to group box
        self.mainSettingGB.setLayout(self.mainFormLayout)

        # likewise, init test settings form layout
        self.testFormLayout = QFormLayout()

        # test settings layout
        self.minExposureTimeTB = QLineEdit("1")
        self.maxExposureTimeTB = QLineEdit("10")
        self.testStepTB = QLineEdit("1")


        # add to form layout
        self.testFormLayout.addRow("Min exposure time (s):", self.minExposureTimeTB)
        self.testFormLayout.addRow("Max exposure time (s):", self.maxExposureTimeTB)
        self.testFormLayout.addRow("Step (s):", self.testStepTB)

        # align items to the left
        self.testFormLayout.setFormAlignment(Qt.AlignLeft)
        self.testFormLayout.setLabelAlignment(Qt.AlignLeft)

        # add form to groupbox
        self.testSettingGB.setLayout(self.testFormLayout)







        # add both boxes to final layout
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.addWidget(self.mainSettingGB)
        self.settingsLayout.addWidget(self.testSettingGB)

        return self.settingsLayout

    def createPreviewTabLayout(self):

        # up buttons
        self.upSmButton = QPushButton("+0.1")
        self.upMdButton = QPushButton("+1")
        self.upLgButton = QPushButton("+10")

        # down buttons
        self.downSmButton = QPushButton("-0.1")
        self.downMdButton = QPushButton("-1")
        self.downLgButton = QPushButton("-10")

        # left buttons
        self.leftSmButton = QPushButton("-0.1")
        self.leftMdButton = QPushButton("-1")
        self.leftLgButton = QPushButton("-10")

        # right buttons
        self.rightSmButton = QPushButton("+0.1")
        self.rightMdButton = QPushButton("+1")
        self.rightLgButton = QPushButton("+10") 
        
        # centre button
        self.centreButton = QPushButton("0") 

        #self.xLabel = QLabel("X")
        #self.xLabel.setAlignment(Qt.AlignCenter)
        #self.yLabel = QLabel("Y")
        #self.yLabel.setAlignment(Qt.AlignCenter)

        # add buttons to grid
        self.arrowGrid = QGridLayout()
        #self.arrowGrid.addWidget(self.xLabel,0,3)
        #self.arrowGrid.addWidget(self.yLabel,4,7)
        self.arrowGrid.addWidget(self.centreButton,4,3)
        self.arrowGrid.addWidget(self.upSmButton,3,3)
        self.arrowGrid.addWidget(self.upMdButton,2,3)
        self.arrowGrid.addWidget(self.upLgButton,1,3)
        self.arrowGrid.addWidget(self.downSmButton,5,3)
        self.arrowGrid.addWidget(self.downMdButton,6,3)
        self.arrowGrid.addWidget(self.downLgButton,7,3)
        self.arrowGrid.addWidget(self.leftSmButton,4,2)
        self.arrowGrid.addWidget(self.leftMdButton,4,1)
        self.arrowGrid.addWidget(self.leftLgButton,4,0)
        self.arrowGrid.addWidget(self.rightSmButton,4,4)
        self.arrowGrid.addWidget(self.rightMdButton,4,5)
        self.arrowGrid.addWidget(self.rightLgButton,4,6)


        # open stream button
        self.openStreamButton = QPushButton("Open Camera Stream")
        self.openStreamButton.clicked.connect(self.openCameraStream)

        # calibrate button
        #self.calibrateButton = QPushButton("Calibrate")  
        #self.calibrateButton.setToolTip("Set zero point for XY stage.") 

        # show XYZ position using text boxes
        #x,y,z = self.stage.getCurrentCoordinates()
        
        self.xTB = QLineEdit()
        self.yTB = QLineEdit()
        self.zTB = QLineEdit()

        self.xyzLayout = QHBoxLayout()
        self.xyzLayout.addWidget(self.xTB)
        self.xyzLayout.addWidget(self.yTB)
        self.xyzLayout.addWidget(self.zTB)
        
        # buttons to set bottom left and top right corners of substrate
        self.setBottomLeftButton = QPushButton("Set Bottom Left")
        self.setBottomLeftButton.setToolTip("Set the coordinates for the bottom left corner of a rectangular substrate. For circular substrates, select two diametrically opposed points.")
        self.setBottomLeftButton.clicked.connect(self.setBottomLeft)
        
        self.setTopRightButton = QPushButton("Set Top Right")
        self.setTopRightButton.setToolTip("Set the coordinates for the top right corner of a rectangular substrate. For circular substrates, select two diametrically opposed points.")
        self.setTopRightButton.clicked.connect(self.setTopRight)
        
        self.calibrationLayout = QHBoxLayout()
        self.calibrationLayout.addWidget(self.setBottomLeftButton)
        self.calibrationLayout.addWidget(self.setTopRightButton)
        


        


        self.previewLayout = QVBoxLayout()
        self.previewLayout.addWidget(self.openStreamButton)
        self.previewLayout.addLayout(self.arrowGrid)
        self.previewLayout.addLayout(self.xyzLayout)
        self.previewLayout.addLayout(self.calibrationLayout)
        #self.previewLayout.addWidget(self.calibrateButton)


        return self.previewLayout






    # LOGIC

    @pyqtSlot()
    def openFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,"Please Select A Photmask", "","BMP Files (*.bmp)", options=options)
        if file:
            self.photomaskTB.setText(file)
            # dos some other stuff here

    @pyqtSlot()
    def openCameraStream(self):
        
        self.cameraPreview.start()
        
    @pyqtSlot()
    def mainEtchLaunch(self):
        
        # disable launch and test buttons, enable cancel button
        self.launchButton.setEnabled(False)
        self.testButton.setEnabled(False)
        self.cancelButton.setEnabled(True)
        
        # pass settings to substrate and photomask
        self.substrate.setShape(str(self.substrateShapeCB.currentText()))
        self.substrate.setBottomLeft()
        self.substrate.setTopRight()
        
        self.photomask.importFile(str(self.photomaskTB.text()))
        self.photomask.split()
        
        exposureTime = float(self.exposureTimeTB.text())
        iterations = int(self.interationsTB.text())
        
        # pass all the settings to the process thread
        self.mainEtchProcess = MainExposure(self.dmd, self.LED, self.stage, self.photomask, self.substrate, exposureTime, iterations)
        
        # connect to progress bar
        self.mainEtchProcess.progress.connect(self.progressBar.setValue)
        self.mainEtchProcess.finished.connect(self.progressBar.reset)
        self.mainEtchProcess.finished.connect(self.resetButtons)
        
        self.mainEtchProcess.start()
        
        
    @pyqtSlot()
    def testEtchLaunch(self):
        
        # disable launch and test buttons, enable cancel button
        self.launchButton.setEnabled(False)
        self.testButton.setEnabled(False)
        self.cancelButton.setEnabled(True)
        
        # pass settings to substrate and photomask
        self.substrate.setShape(str(self.substrateShapeCB.currentText()))
        
        self.substrate.setTopRight()
        
        minExposureTime = float(self.minExposureTimeTB.text())
        maxExposureTime = float(self.maxExposureTimeTB.text())
        step = float(self.testStepTB.text())
        
        # pass all the settings to the process thread
        self.testEtchProcess = TestExposure(self.dmd, self.LED, self.stage, self.substrate, minExposureTime, maxExposureTime, step)
        
        # connect to progress bar
        self.testEtchProcess.progress.connect(self.progressBar.setValue)
        self.testEtchProcess.finished.connect(self.progessBar.reset)
        self.testEtchProcess.finished.connect(self.resetButtons)
        
        self.testEtchProcess.start()
    
    @pyqtSlot()  
    def cancelProcess(self):
        if self.mainEtchProcess.isRunning():
            self.mainEtchProcess.cancel()
        else:
            self.testEtchProcess.cancel()
        
    @pyqtSlot()
    def resetButtons(self):
        # enable launch and test buttons, disable cancel button
        self.launchButton.setEnabled(True)
        self.testButton.setEnabled(True)
        self.cancelButton.setEnabled(False)
    
    
    @pyqtSlot() 
    def setBottomLeft(self):
        # get current coordinates and set the bottom left of the stage
        x,y,z = self.stage.getCurrentCoordinates()
        self.substrate.setBottomLeft(x,y)
        
    @pyqtSlot() 
    def setTopRight(self):
        # get current coordinates and set the bottom left of the stage
        x,y,z = self.stage.getCurrentCoordinates()
        self.substrate.setTopRight(x,y)       


        






 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
