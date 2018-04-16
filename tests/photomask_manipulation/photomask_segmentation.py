from PIL import Image

DMD_WIDTH = 684
DMD_HEIGHT = 608

# use new image for padding
pad = Image.new('RGB',
                 (DMD_WIDTH, DMD_HEIGHT),   # DMD size
                 (0, 0, 0))  # black

# import photomask

photomask = Image.open("photomasks_out.bmp")

# compare size to DMD size
print(photomask.size)

p_width, p_height = photomask.size

# check how many times photomask fits into dmd area
photomask_height_multiplier = (p_height//DMD_HEIGHT)+1
photomask_width_multiplier = (p_width//DMD_WIDTH)+1

# pad out with black so the final image will match the size of the DMD (or a multiple of)
# copy photomask in (top left corner)
pad = pad.resize((photomask_width_multiplier*DMD_WIDTH,photomask_height_multiplier*DMD_HEIGHT))
pad.paste(photomask)

print(pad.size)

pad.save("photomask_large_final.bmp")

# split photomask 
split_photmask = list()

for w in range(photomask_width_multiplier):
	for h in range(photomask_height_multiplier):
		split_photmask.append(pad.crop((w*DMD_WIDTH,h*DMD_HEIGHT,(w+1)*DMD_WIDTH,(h+1)*DMD_HEIGHT)))

i = 0

for subsection in split_photmask:
	subsection.save("photmask_subsection_" + str(i) +".bmp")
	i += 1




	






