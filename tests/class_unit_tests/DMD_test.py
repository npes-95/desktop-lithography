import sys
sys.path.append("../../lib/helper")

from DMD import LightCrafter

dmd = LightCrafter()

print(dmd.getVersion())

#dmd.setImage("../prelim_tests/photomask_manipulation/photomask_small_final.bmp")
dmd.setTestPattern()
