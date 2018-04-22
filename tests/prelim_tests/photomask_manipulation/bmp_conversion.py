import cairosvg
from PIL import Image


# use cairosvg library to convert svg files to a format readable by pillow (PIL fork, good for image manipulation and conversion)
cairosvg.svg2png(url="Photomasks_Bigger_clearance.svg", write_to="photomasks_out.png")

# read in this new file, edit and convert to bmp (PIL can read PDFs and most other formats - just need the extra step for .svg)
im = Image.open("photomasks_out.png")

print(im.size)

im.save("photomasks_out.bmp")

# the bmp can then be sent to the DMD