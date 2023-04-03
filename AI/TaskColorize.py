#############################################################################
#
#   Source from:
#   https://github.com/leonelhs/neural-colorization
#   Forked from:
#   https://github.com/zeruniverse/neural-colorization
#   Reimplemented by: Leonel Hernández
#
##############################################################################


import PIL.Image
import cv2
import numpy as np
import torch
from scipy.ndimage import zoom
from skimage.color import rgb2yuv, yuv2rgb
from torch.autograd import Variable
from AI.colorize.model import generator
from Tasks.TaskPhotoEnhancer import TaskPhotoEnhancer

model_path = "./models/colorize.pth"


class TaskColorize(TaskPhotoEnhancer):

    def __init__(self, threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress):
        super().__init__(threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.gen = generator()
        self.gen.load_state_dict(torch.load(model_path, map_location=device))

    def executeEnhanceWork(self, image, progress_callback):
        img_yuv = rgb2yuv(image)
        H, W, _ = img_yuv.shape
        infimg = np.expand_dims(np.expand_dims(img_yuv[..., 0], axis=0), axis=0)
        img_variable = Variable(torch.Tensor(infimg - 0.5))
        if torch.cuda.is_available():
            img_variable = img_variable.cuda("0")
        res = self.gen(img_variable)
        uv = res.cpu().detach().numpy()
        uv[:, 0, :, :] *= 0.436
        uv[:, 1, :, :] *= 0.615
        (_, _, H1, W1) = uv.shape
        uv = zoom(uv, (1, 1, H / H1, W / W1))
        yuv = np.concatenate([infimg, uv], axis=1)[0]
        rgb = yuv2rgb(yuv.transpose(1, 2, 0))
        result = (rgb.clip(min=0, max=1) * 256)[:, :, [2, 1, 0]]
        cv2.imwrite("./output.png", result)
        return PIL.Image.open("./output.png")
        # return PIL.Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
