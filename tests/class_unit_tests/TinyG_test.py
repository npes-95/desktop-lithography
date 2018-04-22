from TinyG import MotorDriver

stage = MotorDriver()

print(stage.writeGCodeLine("G1 f400 Y-10"))
