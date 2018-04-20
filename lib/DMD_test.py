from DMD import LightCrafter

dmd = LightCrafter()

#print(dmd.getVersion())

with open("../tests/photomask_manipulation/photomask_small_final.bmp", "rb") as bmp:
	dmd.setImage(bmp.read())
