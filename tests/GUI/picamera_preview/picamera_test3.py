import sys
import io
import picamera
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal, QThread
from PIL import Image, ImageQt

class videoThread(QThread):
    
    newFrame = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        

    def run(self):
        
        with picamera.PiCamera() as camera:
            
            time.sleep(2)
            frame = io.BytesIO()
        
            while(True):
                
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
                
                time.sleep(0.07)

class PiCameraPreview(QMainWindow):

    def __init__(self):
        super().__init__()

        #video stream
        self.video = videoThread()
        
        # connect to slot
        self.video.newFrame.connect(self.setFrame)
        
        #create label
        self.label = QLabel(self)
        
        self.show()
        
        self.video.start()
        

        
    
    @pyqtSlot(QImage)
    def setFrame(self,frame):
        pixmap = QPixmap.fromImage(frame)
        self.label.setPixmap(pixmap)
        self.label.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PiCameraPreview()
    sys.exit(app.exec_())
