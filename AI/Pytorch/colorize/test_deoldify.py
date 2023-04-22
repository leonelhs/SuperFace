import PIL.Image
from AI.Pytorch.colorize.deoldify.filters import BaseFilter

filtr = BaseFilter()
filtr.model.eval()

source_path = '/home/leonel/goyo-zero.png'

orig_image = PIL.Image.open(source_path).convert('RGB')
image = filtr.filter(orig_image)

image.save("/home/leonel/goyo-color.jpg")

