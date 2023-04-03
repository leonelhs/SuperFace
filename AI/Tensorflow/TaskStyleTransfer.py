#############################################################################
#
#   Source from:
#   https://www.tensorflow.org/hub/tutorials/tf2_arbitrary_image_stylization
#   Forked from:
#   Reimplemented by: Leonel Hernández
#
##############################################################################

import PIL.Image
import numpy as np
import tensorflow as tf

from Tasks.TaskPhotoEnhancer import TaskPhotoEnhancer

print("TF Version: ", tf.__version__)
print("Eager mode enabled: ", tf.executing_eagerly())
print("GPU available: ", tf.config.list_physical_devices('GPU'))


def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image


def load_image(image_path, image_size=(256, 256)):
    """Loads and preprocesses images."""
    img = tf.io.decode_image(
        tf.io.read_file(image_path),
        channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img


def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


model_path = "./models/image-stylization-v1-256"


class TaskStyleTransfer(TaskPhotoEnhancer):

    def __init__(self, threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress):
        super().__init__(threadpool, enhanceDone, enhanceComplete, trackEnhanceProgress)
        self.model = tf.saved_model.load(model_path)
        self.content_image = None
        self.style_image = None

    def executeEnhanceWork(self, image, progress_callback):
        content_image = load_image(self.content_image, (384, 384))
        style_image = load_image(self.style_image, (256, 256))
        style_image = tf.nn.avg_pool(style_image, ksize=[3, 3], strides=[1, 1], padding='SAME')
        stylized_image = self.model(tf.constant(content_image), tf.constant(style_image))[0]
        return tensor_to_image(stylized_image[0])
