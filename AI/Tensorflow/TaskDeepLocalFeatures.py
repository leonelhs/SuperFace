#############################################################################
#
#   Source from:
#   https://www.tensorflow.org/hub/tutorials/tf_hub_delf_module
#   Forked from:
#   https://www.tensorflow.org/hub/tutorials/tf_hub_delf_module
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import PIL.Image
from PIL import Image, ImageOps
from scipy.spatial import cKDTree
from skimage.feature import plot_matches
from skimage.measure import ransac
from skimage.transform import AffineTransform

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer


def match_images(image1, image2, result1, result2):
    distance_threshold = 0.8

    # Read features.
    num_features_1 = result1['locations'].shape[0]
    print("Loaded image 1's %d features" % num_features_1)

    num_features_2 = result2['locations'].shape[0]
    print("Loaded image 2's %d features" % num_features_2)

    # Find nearest-neighbor matches using a KD tree.
    d1_tree = cKDTree(result1['descriptors'])
    _, indices = d1_tree.query(
        result2['descriptors'],
        distance_upper_bound=distance_threshold)

    # Select feature locations for putative matches.
    locations_2_to_use = np.array([
        result2['locations'][i, ]
        for i in range(num_features_2)
        if indices[i] != num_features_1
    ])
    locations_1_to_use = np.array([
        result1['locations'][indices[i], ]
        for i in range(num_features_2)
        if indices[i] != num_features_1
    ])

    # Perform geometric verification using RANSAC.
    _, inliers = ransac(
        (locations_1_to_use, locations_2_to_use),
        AffineTransform,
        min_samples=3,
        residual_threshold=20,
        max_trials=1000)

    print('Found %d inliers' % sum(inliers))

    # Visualize correspondences.
    _, ax = plt.subplots()
    inlier_idxs = np.nonzero(inliers)[0]
    stack = np.column_stack((inlier_idxs, inlier_idxs))
    plot_matches(
        ax,
        image1,
        image2,
        locations_1_to_use,
        locations_2_to_use,
        stack,
        matches_color='b')
    ax.axis('off')
    ax.set_title('DELF correspondences')

    return PIL.Image.fromarray(stack)


def openFitImage(image_path, width=256, height=256):
    image = Image.open(image_path)
    image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
    return image


model_path = "./models/delf"


class TaskDeepLocalFeatures(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.model = tf.saved_model.load(model_path).signatures['default']
        self.image_a = None
        self.image_b = None

    def setImageA(self, image):
        self.image_a = openFitImage(image)

    def setImageB(self, image):
        self.image_b = openFitImage(image)

    def run_delf(self, image):
        np_image = np.array(image)
        float_image = tf.image.convert_image_dtype(np_image, tf.float32)

        return self.model(
            image=float_image,
            score_threshold=tf.constant(100.0),
            image_scales=tf.constant([0.25, 0.3536, 0.5, 0.7071, 1.0, 1.4142, 2.0]),
            max_feature_num=tf.constant(1000))

    def executeEnhanceWork(self, images, progress_callback):
        result_a = self.run_delf(self.image_a)
        result_b = self.run_delf(self.image_b)
        match = match_images(self.image_a, self.image_b, result_a, result_b)
        # Fixme: return match images
        return match
