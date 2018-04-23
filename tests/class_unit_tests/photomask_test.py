import sys
sys.path.append('../../lib/')
from photomask import Photomask

photomask = Photomask()

photomask.importFile("../prelim_tests/photomask_manipulation/Photomasks_Bigger_clearance.svg")

photomask.split()
