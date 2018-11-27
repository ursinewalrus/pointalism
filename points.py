from PIL import Image
from Tkinter import Tk
from tkFileDialog import askopenfilename
import math
import painter

file_path = askopenfilename()

painter = painter.Painter(4, False, file_path, False)
painter.paint_picture_with_points()
a = 1