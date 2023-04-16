#############################################################################
#
#   Source from:
#   https://keras.io/examples/vision/deeplabv3_plus/
#   Forked from:
#   https://keras.io/examples/vision/deeplabv3_plus/
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import PIL.Image
from PIL import Image as Image
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer

model_path = './models/deeplabv3p-resnet50'

colormap = np.array([[0, 0, 0], [31, 119, 180], [44, 160, 44], [44, 127, 125], [52, 225, 143],
                     [217, 222, 163], [254, 128, 37], [130, 162, 128], [121, 7, 166], [136, 183, 248],
                     [85, 1, 76], [22, 23, 62], [159, 50, 15], [101, 93, 152], [252, 229, 92],
                     [167, 173, 17], [218, 252, 252], [238, 126, 197], [116, 157, 140], [214, 220, 252]],
                    dtype=np.uint8)

img_size = 512


def array2image(ndarray):
    return PIL.Image.fromarray(np.uint8(ndarray)).convert('RGB')


def decode_segmentation_masks(mask, colormap, n_classes):
    r = np.zeros_like(mask).astype(np.uint8)
    g = np.zeros_like(mask).astype(np.uint8)
    b = np.zeros_like(mask).astype(np.uint8)
    for l in range(0, n_classes):
        idx = mask == l
        r[idx] = colormap[l, 0]
        g[idx] = colormap[l, 1]
        b[idx] = colormap[l, 2]
    rgb = np.stack([r, g, b], axis=2)
    return rgb


def get_overlay(image, colored_mask):
    image = tf.keras.preprocessing.image.array_to_img(image)
    image = np.array(image).astype(np.uint8)
    overlay = cv2.addWeighted(image, 0.35, colored_mask, 0.65, 0)
    return overlay


def vis_parsing_maps(im, parsing_anno, stride=1):
    # Colors for all 20 parts
    part_colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0],
                   [255, 0, 85], [255, 0, 170],
                   [0, 255, 0], [85, 255, 0], [170, 255, 0],
                   [0, 255, 85], [0, 255, 170],
                   [0, 0, 255], [85, 0, 255], [170, 0, 255],
                   [0, 85, 255], [0, 170, 255],
                   [255, 255, 0], [255, 255, 85], [255, 255, 170],
                   [255, 0, 255], [255, 85, 255], [255, 170, 255],
                   [0, 255, 255], [85, 255, 255], [170, 255, 255]]

    im = np.array(im)
    vis_im = im.copy().astype(np.uint8)
    vis_parsing_anno = parsing_anno.copy().astype(np.uint8)
    vis_parsing_anno = cv2.resize(vis_parsing_anno, None, fx=stride, fy=stride, interpolation=cv2.INTER_NEAREST)
    vis_parsing_anno_color = np.zeros((vis_parsing_anno.shape[0], vis_parsing_anno.shape[1], 3)) + 255

    num_of_class = np.max(vis_parsing_anno)

    for pi in range(1, num_of_class + 1):
        index = np.where(vis_parsing_anno == pi)
        vis_parsing_anno_color[index[0], index[1], :] = part_colors[pi]

    vis_parsing_anno_color = vis_parsing_anno_color.astype(np.uint8)
    vis_im = cv2.addWeighted(cv2.cvtColor(vis_im, cv2.COLOR_RGB2BGR), 0.4, vis_parsing_anno_color, 0.6, 0)

    return vis_parsing_anno, vis_im


class TaskSegmentation(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.model = load_model(model_path)

    def infer(self, image_tensor):
        predictions = self.model.predict(np.expand_dims(image_tensor, axis=0))
        predictions = np.squeeze(predictions)
        predictions = np.argmax(predictions, axis=2)
        return predictions

    def executeEnhanceWork(self, image: Image, progress_callback):
        progress_callback.emit(".")
        image = tf.convert_to_tensor(image)
        image = tf.image.resize(images=image, size=[img_size, img_size])
        image = image / 127.5 - 1
        prediction_mask = self.infer(image_tensor=image)
        prediction_colormap = decode_segmentation_masks(prediction_mask, colormap, 20)
        overlay = get_overlay(image, prediction_colormap)
        return prediction_mask, prediction_colormap, overlay
        # return vis_parsing_maps(image, prediction_mask)
        # return prediction_mask
