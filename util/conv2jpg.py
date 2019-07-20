from pdf2image import convert_from_path
import os
pdf = os.getcwd().split('/')[-1] + '.pdf'
jpg = os.getcwd().split('/')[-1] + '.jpg'
images = convert_from_path(pdf)
images[0].save(jpg)