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
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

from Tasks.TaskPhotoEnhancer import TaskPhotoEnhancer

model_path = './models/deeplabv3p-resnet50'

colormap = np.array([[0, 0, 0], [31, 119, 180], [44, 160, 44], [44, 127, 125], [52, 225, 143],
                     [217, 222, 163], [254, 128, 37], [130, 162, 128], [121, 7, 166], [136, 183, 248],
                     [85, 1, 76], [22, 23, 62], [159, 50, 15], [101, 93, 152], [252, 229, 92],
                     [167, 173, 17], [218, 252, 252], [238, 126, 197], [116, 157, 140], [214, 220, 252]],
                    dtype=np.uint8)

img_size = 512


def infer(model, image_tensor):
    predictions = model.predict(np.expand_dims((image_tensor), axis=0))
    predictions = np.squeeze(predictions)
    predictions = np.argmax(predictions, axis=2)
    return predictions


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


class TaskSegmentation(TaskPhotoEnhancer):

    def __init__(self, threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress):
        super().__init__(threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress)
        self.model = load_model(model_path)

    def executeEnhanceWork(self, image, progress_callback):
        image = tf.convert_to_tensor(image)
        image = tf.image.resize(images=image, size=[img_size, img_size])
        image = image / 127.5 - 1
        prediction_mask = infer(image_tensor=image, model=self.model)
        prediction_colormap = decode_segmentation_masks(prediction_mask, colormap, 20)
        overlay = get_overlay(image, prediction_colormap)
        return PIL.Image.fromarray(overlay)
