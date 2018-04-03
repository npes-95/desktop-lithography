from PIL import Image

DMD_WIDTH = 684
DMD_HEIGHT = 608

# use new image for padding
pad = Image.new('RGB',
                 (DMD_WIDTH, DMD_HEIGHT),   # DMD size
                 (0, 0, 0))  # black

# import photomask

photomask = Image.open("photomask_large.bmp")

# compare size to DMD size
print(photomask.size)

p_width, p_height = photomask.size

if p_width < DMD_WIDTH and p_height < DMD_HEIGHT:


	# pad out with black so the final image will match the size of the DMD
	# copy photomask in (top left corner)
	pad.paste(photomask)
	pad.save("photomask_small_final.bmp")


elif p_width > DMD_WIDTH or p_height > DMD_HEIGHT:

	# pad out with black to a rectangle four times the size of the DMD
	# this will be split, and the edges of the design will match up
	pad = pad.resize((2*DMD_WIDTH,2*DMD_HEIGHT))

	print(pad.size)

	# copy photomask in (top left corner)
	pad.paste(photomask)

	# split this photomask into 4 (left to right, top to bottom)
	photomask_quad1 = pad.crop((0,0,DMD_WIDTH,DMD_HEIGHT))
	photomask_quad2 = pad.crop((DMD_WIDTH,0,2*DMD_WIDTH,DMD_HEIGHT))
	photomask_quad3 = pad.crop((0,DMD_HEIGHT,DMD_WIDTH,2*DMD_HEIGHT))
	photomask_quad4 = pad.crop((DMD_WIDTH,DMD_HEIGHT,2*DMD_WIDTH,2*DMD_HEIGHT))  

	pad.save("photomask_large_final.bmp")
	photomask_quad1.save("photomask_quad1_final.bmp")
	photomask_quad2.save("photomask_quad2_final.bmp")
	photomask_quad3.save("photomask_quad3_final.bmp")
	photomask_quad4.save("photomask_quad4_final.bmp")


	






