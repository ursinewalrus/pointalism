from PIL import Image
from Tkinter import Tk
from tkFileDialog import askopenfilename
import math
import painter

file_path = askopenfilename()

painter = painter.Painter(5, False, file_path)
p = painter.find_point_average_rgb()
a = 1