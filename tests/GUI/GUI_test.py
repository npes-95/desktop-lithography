import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QTabWidget, QVBoxLayout, QLineEdit, QFormLayout, QComboBox, QGroupBox
from PyQt5.QtGui import QIcon
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = "Desktop Lithography Control Software - 1.0"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):

        # basic window geometry
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # init tabs
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)


        self.show()


class TableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.launchTab = QWidget()   
        self.settingsTab = QWidget()
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.launchTab,"Launch")
        self.tabs.addTab(self.settingsTab,"Settings")

        # create launch tab contents
        self.createLaunchTabContents()

        # create first tab
        self.launchTab.layout = self.launchLayout
        self.launchTab.setLayout(self.launchTab.layout)

        # create settings tab contents
        self.createSettingsTabContents()

        # create second tab
        self.settingsTab.layout = self.settingsLayout
        self.settingsTab.setLayout(self.settingsTab.layout)
 
        # Add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def createLaunchTabContents(self):

        # launch button 
        self.launchButton = QPushButton("Launch")
        self.launchButton.setToolTip("Launch photolithogrphy operation.")

        self.testButton = QPushButton("Test")
        self.testButton.setToolTip("Test photolithogrphy operation. Will print identical pattern at different exposure times.")

        self.launchLayout = QVBoxLayout(self)
        self.launchLayout.addWidget(self.launchButton)
        self.launchLayout.addWidget(self.testButton)



        # add picamera stream in first tab?

    def createSettingsTabContents(self):

        # init group boxes
        self.mainSettingGB = QGroupBox("Main")
        self.testSettingGB = QGroupBox("Test")

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


        # add elements to form layout
        self.mainFormLayout.addRow("Exposure time (s):", self.exposureTimeTB)
        self.mainFormLayout.addRow("Pattern iterations:", self.interationsTB)
        self.mainFormLayout.addRow("Substrate diameter:", self.substrateDiameterTB)
        self.mainFormLayout.addRow("Substrate shape:", self.substrateShapeCB)

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

        # add form to groupbox
        self.testSettingGB.setLayout(self.testFormLayout)



        # add both boxes to final layout
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.addWidget(self.mainSettingGB)
        self.settingsLayout.addWidget(self.testSettingGB)

        






 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())