#############################################################################
#
#   Source from:
#   https://www.tensorflow.org/hub/tutorials/movenet
#   Forked from:
#   https://www.tensorflow.org/hub/tutorials/movenet
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import PIL.Image
import PIL.ImageOps
import numpy as np
import tensorflow as tf
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor, QPainter

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer

# Dictionary that maps from joint names to keypoint indices.
KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1, 'right_eye': 2,
    'left_ear': 3, 'right_ear': 4,
    'left_shoulder': 5, 'right_shoulder': 6,
    'left_elbow': 7, 'right_elbow': 8,
    'left_wrist': 9, 'right_wrist': 10,
    'left_hip': 11, 'right_hip': 12,
    'left_knee': 13, 'right_knee': 14,
    'left_ankle': 15, 'right_ankle': 16
}

COLOR_DICT = {
    (0, 1): 'Magenta',
    (0, 2): 'Cyan',
    (1, 3): 'Magenta',
    (2, 4): 'Cyan',
    (0, 5): 'Magenta',
    (0, 6): 'Cyan',
    (5, 7): 'Magenta',
    (7, 9): 'Magenta',
    (6, 8): 'Cyan',
    (8, 10): 'Cyan',
    (5, 6): 'Yellow',
    (5, 11): 'Magenta',
    (6, 12): 'Cyan',
    (11, 12): 'Yellow',
    (11, 13): 'Magenta',
    (13, 15): 'Magenta',
    (12, 14): 'Cyan',
    (14, 16): 'Cyan'
}


def process_keypoints(keypoints, height, width, threshold=0.11):
    """Returns high confidence keypoints and edges for visualization.

      Args:
        keypoints: A numpy array with shape [1, 1, 17, 3] representing
          the keypoint coordinates and scores returned from the MoveNet model.
        height: height of the image in pixels.
        width: width of the image in pixels.
        threshold: minimum confidence score for a keypoint to be
          visualized.

      Returns:
        A (joints, bones, colors) containing:
          * the coordinates of all keypoints of all detected entities;
          * the coordinates of all skeleton edges of all detected entities;
          * the colors in which the edges should be plotted.
      """
    keypoints_all = []
    keypoint_edges_all = []
    colors = []
    num_instances, _, _, _ = keypoints.shape
    for idx in range(num_instances):
        kpts_x = keypoints[0, idx, :, 1]
        kpts_y = keypoints[0, idx, :, 0]
        kpts_scores = keypoints[0, idx, :, 2]
        kpts_absolute_xy = np.stack(
            [width * np.array(kpts_x), height * np.array(kpts_y)], axis=-1)
        kpts_above_thresh_absolute = kpts_absolute_xy[
                                     kpts_scores > threshold, :]
        keypoints_all.append(kpts_above_thresh_absolute)

        for edge_pair, color in COLOR_DICT.items():
            if (kpts_scores[edge_pair[0]] > threshold and
                    kpts_scores[edge_pair[1]] > threshold):
                x_start = kpts_absolute_xy[edge_pair[0], 0]
                y_start = kpts_absolute_xy[edge_pair[0], 1]
                x_end = kpts_absolute_xy[edge_pair[1], 0]
                y_end = kpts_absolute_xy[edge_pair[1], 1]
                line_seg = np.array([[x_start, y_start], [x_end, y_end]])
                keypoint_edges_all.append(line_seg)
                colors.append(color)
    if keypoints_all:
        joints = np.concatenate(keypoints_all, axis=0)
    else:
        joints = np.zeros((0, 17, 2))

    if keypoint_edges_all:
        bones = np.stack(keypoint_edges_all, axis=0)
    else:
        bones = np.zeros((0, 2, 2))
    return joints, bones, colors


def draw_bones(pixmap, height, width, keypoints):
    painter = QPainter(pixmap)
    joints, bones, colors = process_keypoints(keypoints, height, width)

    for bone, color in zip(bones.tolist(), colors):
        pen = QPen(QColor(color), 4, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(*bone[0], *bone[1])

    radio = 3
    pen = QPen(QColor("Red"), 5, Qt.SolidLine)
    painter.setPen(pen)
    for c_x, c_y in joints:
        painter.drawEllipse(c_x - radio, c_y - radio, radio * 2, radio * 2)


input_size = 256
model_path = "./models/movenet"


class TaskEstimatePose(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.model = tf.saved_model.load(model_path).signatures['serving_default']

    def movenet(self, image):
        """Runs detection on an input image.

            Args:
              image: A [1, height, width, 3] tensor represents the input image
                pixels. Note that the height/width should already be resized and match the
                expected input resolution of the model before passing into this function.

            Returns:
              A [1, 1, 17, 3] float numpy array representing the predicted keypoint
              coordinates and scores.
        """
        image = tf.cast(image, dtype=tf.int32)
        outputs = self.model(image)
        return outputs['output_0'].numpy()

    def executeEnhanceWork(self, image_path, progress_callback):
        size = (1280, 1280)
        image = tf.io.read_file(image_path)
        image = tf.image.decode_jpeg(image)
        input_image = tf.expand_dims(image, axis=0)
        input_image = tf.image.resize_with_pad(input_image, input_size, input_size)
        keypoints = self.movenet(input_image)
        # Visualize the predictions with image.
        image = PIL.Image.open(image_path)
        # Fixme: accurate match bones and image
        image = PIL.ImageOps.fit(image, size, PIL.Image.LANCZOS)
        pixmap = image.toqpixmap()
        draw_bones(pixmap, size, keypoints)
        return pixmap
