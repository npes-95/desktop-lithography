import sys
import io
import picamera
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PIL import Image, ImageQt

class videoThread(QThread):
    
    newFrame = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        #self.finished.connect(self.deleteLater)
        
    def __del__(self):
        self.wait()
        

    def run(self):
        
        frame = io.BytesIO()
        self.running = True
        
        with picamera.PiCamera() as camera:
            
            # increase camera framerate and reduce resolution to reduce capture speed
            camera.resolution = (640,480)
            camera.framerate = 80
            
            time.sleep(2)
            
        
            while(self.running):
                
                # capture image
                camera.capture(frame, 'jpeg')
                
                # convert stream to PIL and Qt image
                frame.seek(0)
                pframe = Image.open(frame)
                qframe = ImageQt.ImageQt(pframe)
                
                self.newFrame.emit(qframe)
                
                # reset stream
                frame.seek(0)
                frame.truncate()
                
                #time.sleep(0.04)
            
            print("Preview thread exiting.")
    
    @pyqtSlot()            
    def stop(self):
        self.running = False
                
      

class PiCameraPreview(QMainWindow):
    
    windowClosed = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.isOpen = False
        
        #create label
        self.label = QLabel(self)
        self.label.setText("Please wait, camera is warming up...")
        
        self.setWindowTitle("Preview")
        self.setGeometry(650, 30, 640, 480)
        self.label.adjustSize()
        
        #self.show()
        
        #self.video.start()
        

        
        
        
        
    def start(self): 
        
        #video stream
        self.video = videoThread()
        
        # connect new frame signal to frame update slot
        self.video.newFrame.connect(self.setFrame)
        
        # connect window closed signal to strop thread slot
        self.windowClosed.connect(self.video.stop)  
           
        self.isOpen = True
        self.show()
        self.video.start()
        
    def closeEvent(self, event):
        self.isOpen = False
        self.windowClosed.emit()
        

        
        
        
        

        
    
    @pyqtSlot(QImage)
    def setFrame(self,frame):
        pixmap = QPixmap.fromImage(frame)
        self.label.setPixmap(pixmap)
        self.label.adjustSize()


#if __name__ == '__main__':
 #   app = QApplication(sys.argv)
 #   ex = PiCameraPreview()
 #   sys.exit(app.exec_())
