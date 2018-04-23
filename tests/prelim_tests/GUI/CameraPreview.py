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
        
    def __del__(self):
        self.wait()
        

    def run(self):
        
        frame = io.BytesIO()
        self.running = True
        self.paused = True
        
        # init camera here (we want it to be closed when the preview exits, so other processes can use it)
        camera = picamera.PiCamera()
               
        # increase camera framerate and reduce resolution to reduce capture speed
        camera.resolution = (640,480)
        camera.framerate = 80
            
        time.sleep(2)
            
        
        while(self.running):
            
            if(self.paused):
                
                camera.close()
                
                while(self.paused):
                    time.sleep(0.1)
                
                camera = picamera.PiCamera()
                camera.resolution = (640,480)
                camera.framerate = 80
                time.sleep(0.1)
                
                
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
                
            time.sleep(0.04)
            
        camera.close()

            
        print("Preview thread exiting.")
              
    def stop(self):
        self.running = False
        
        
    def play(self):
        self.paused = False
        
    def pause(self):
        self.paused = True
                
      

class PiCameraPreview(QWidget):

    def __init__(self):
        super().__init__()
        
        self.isOpen = False
        
        #create label
        self.label = QLabel(self)
        self.label.setText("Please wait, camera is warming up...")
        
        self.setWindowTitle("Preview")
        self.setGeometry(650, 30, 640, 480)
        self.label.adjustSize()
        
        
        #video stream
        self.video = videoThread()
        
        # connect new frame signal to frame update slot
        self.video.newFrame.connect(self.setFrame) 
            
        self.video.start()
        
        
    def __del__(self):
        self.video.stop()
        if self.video.isRunning():
            self.video.wait()
        
        
    def start(self): 
        self.video.play()           
        self.isOpen = True
        self.show()
        
        
    def closeEvent(self, event):
        self.video.pause()        
        self.isOpen = False
  
    
    @pyqtSlot(QImage)
    def setFrame(self,frame):
        pixmap = QPixmap.fromImage(frame)
        self.label.setPixmap(pixmap)
        self.label.adjustSize()


#if __name__ == '__main__':
 #   app = QApplication(sys.argv)
 #   ex = PiCameraPreview()
 #   sys.exit(app.exec_())
