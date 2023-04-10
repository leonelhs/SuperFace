#############################################################################
#
#   Source from:
#   https://github.com/leonelhs/face-makeup.PyTorch
#   Forked from:
#   https://github.com/zllrunning/face-makeup.PyTorch
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import PIL.Image
import cv2
import numpy as np
from skimage.filters import gaussian

from AI.TaskFaceParser import TaskFaceParser


def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5)

    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img

    img_out = img_out / 255.0

    mask_1 = img_out < 0
    mask_2 = img_out > 1

    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255
    return np.array(img_out, dtype=np.uint8)


def hair(image, parsing, part=17, color=[230, 50, 20]):
    b, g, r = color  # [10, 50, 250]       # [10, 250, 10]
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part == 12 or part == 13:
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    else:
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    if part == 17:
        changed = sharpen(changed)

    try:
        changed[parsing != part] = image[parsing != part]
    except IndexError:
        raise Exception("Not able to parse face")
    return changed


# 1  face
# 11 teeth
# 12 upper lip
# 13 lower lip
# 17 hair


class TaskFaceMakeup(TaskFaceParser):
    def __init__(self, args):
        super().__init__(args)

    def executeEnhanceWork(self, image, progress_callback):
        parsing, dark_mask, color_mask = self.parseFace(image)
        image = np.array(image)
        parsing = cv2.resize(parsing, image.shape[0:2], interpolation=cv2.INTER_NEAREST)

        table = {
            'hair': 17,
            'upper_lip': 12,
            'lower_lip': 13
        }

        parts = [table['hair'], table['upper_lip'], table['lower_lip']]

        colors = [[230, 50, 20], [20, 70, 180], [20, 70, 180]]

        for part, color in zip(parts, colors):
            image = hair(image, parsing, part, color)

        image = cv2.resize(image, (512, 512))
        return PIL.Image.fromarray(image)
