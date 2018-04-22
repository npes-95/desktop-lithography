# HELPER CLASS FOR PHOTOMASK

import cairosvg
from PIL import Image

class Photomask():

	def __init__(self):

		self.dmdPixelWidth = 684
		self.dmdPixelHeight = 608

		# list in case the photomask has to be split into multiple files
		self.photomaskFiles = list()


	def importFile(self, file):

		# import file and convert to correct format

		if file.lower().endswith('.svg'):

			cairosvg.svg2png(url=file, write_to="../temp/photmask_temp.png")
			im = Image.open("../temp/photmask_temp.png")
			im.save("../temp/raw_photmask.bmp")
			im.close()

		else:

			im = Image.open(file)
			im.save("../temp/raw_photmask.bmp")
			im.close()

	def split(self):

		# empty list
		self.photmaskFiles[:] = []

		# use new image for padding
		pad = Image.new('RGB',
                 (self.dmdPixelWidth, self.dmdPixelHeight),   # DMD size
                 (0, 0, 0))  # black

		# import converted photomask
		rawPhotomask = Image.open("../temp/raw_photmask.bmp")

		# get its size
		rp_width, rp_height = rawPhotomask.size

		# check how many times photomask fits into dmd area
		photomask_width_multiplier = (rp_width//self.dmdPixelWidth)+1
		photomask_height_multiplier = (rp_height//self.dmdPixelHeight)+1

		# pad out with black so the final image will match the size of the DMD (or a multiple of)
		# copy photomask in (top left corner)
		pad = pad.resize((photomask_width_multiplier*self.dmdPixelWidth,photomask_height_multiplier*self.dmdPixelHeight))
		pad.paste(rawPhotomask)

		# split photomask 
		split_photomask = list()

		for w in range(photomask_width_multiplier):
			for h in range(photomask_height_multiplier):
				split_photomask.append(pad.crop((w*self.dmdPixelWidth,h*self.dmdPixelHeight,(w+1)*self.dmdPixelWidth,(h+1)*self.dmdPixelHeight)))

		i = 0

		for subsection in split_photomask:
			filepath = "temp/photomask_final" + str(i) +".bmp"
			photomaskFiles.append(filepath)
			subsection.save("../" + filepath)
			i += 1

		rawPhotomask.close()

	def getFiles(self):

		return self.photomaskFiles


		



