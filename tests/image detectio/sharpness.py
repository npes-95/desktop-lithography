from PIL import Image
import numpy as np

filename = r'H:\My Documents\5th year programming\fix-blur-photo-featured.jpg' #blurry image
filename2 = r'H:\My Documents\5th year programming\how-to-get-sharp-landscapes-images-gavin-hardcastle.jpg' #sharp image

im = Image.open(filename).convert('L') # to grayscale
array = np.asarray(im, dtype=np.int32)

gy, gx = np.gradient(array)
gnorm = np.sqrt(gx**2 + gy**2)

#higher value of sharpness = in-focus image

sharpness = np.average(gnorm)
print(sharpness)

im = Image.open(filename2).convert('L') # to grayscale
array = np.asarray(im, dtype=np.int32)

gy, gx = np.gradient(array)
gnorm = np.sqrt(gx**2 + gy**2)
sharpness2 = np.average(gnorm)
print(sharpness2)
