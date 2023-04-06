#############################################################################
#
#   Source from:
#   https://github.com/leonelhs/baldgan
#   Forked from:
#   https://github.com/david-svitov/baldgan
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import os

import PIL.Image
import cv2
import numpy as np
from retinaface import RetinaFace
from skimage import transform as trans

from AI.baldgan.model import buildModel
from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
gpu_id = -1

image_size = [256, 256]

src = np.array([
    [30.2946, 51.6963],
    [65.5318, 51.5014],
    [48.0252, 71.7366],
    [33.5493, 92.3655],
    [62.7299, 92.2041]], dtype=np.float32)

src[:, 0] += 8.0
src[:, 0] += 15.0
src[:, 1] += 30.0
src /= 112
src *= 200


def list2array(values):
    return np.array(list(values))


def align_face(img):
    faces = RetinaFace.detect_faces(img)
    bounding_boxes = np.array([list2array(faces[face]['facial_area']) for face in faces])
    points = np.array([list2array(faces[face]['landmarks'].values()) for face in faces])
    white_image = np.ones(img.shape, dtype=np.uint8) * 255

    result_faces = []
    result_masks = []
    result_matrix = []

    if bounding_boxes.shape[0] > 0:
        det = bounding_boxes[:, 0:4]
        for i in range(det.shape[0]):
            _det = det[i]
            dst = points[i]

            tform = trans.SimilarityTransform()
            tform.estimate(dst, src)
            M = tform.params[0:2, :]
            warped = cv2.warpAffine(img, M, (image_size[1], image_size[0]), borderValue=0.0)
            mask = cv2.warpAffine(white_image, M, (image_size[1], image_size[0]), borderValue=0.0)

            result_faces.append(warped)
            result_masks.append(mask)
            result_matrix.append(tform.params[0:3, :])

    return result_faces, result_masks, result_matrix


def put_face_back(img, faces, masks, result_matrix):
    for i in range(len(faces)):
        M = np.linalg.inv(result_matrix[i])[0:2]
        warped = cv2.warpAffine(faces[i], M, (img.shape[1], img.shape[0]), borderValue=0.0)
        mask = cv2.warpAffine(masks[i], M, (img.shape[1], img.shape[0]), borderValue=0.0)
        mask = mask // 255
        img = img * (1 - mask)
        img = img.astype(np.uint8)
        img += warped * mask
    return img


model_path = './models/faces_bald_InsNorm_4x4_D2/model_G_5_170.hdf5'


class TaskBaldFace(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.model = buildModel()
        self.model.load_weights(model_path)

    def executeEnhanceWork(self, image, progress_callback):
        image = np.array(image)
        faces, masks, matrix = align_face(image)
        result_faces = []

        for face in faces:
            input_face = np.expand_dims(face, axis=0)
            input_face = input_face / 127.5 - 1.
            result = self.model.predict(input_face)[0]
            result = ((result + 1.) * 127.5)
            result = result.astype(np.uint8)
            result_faces.append(result)

        img_result = put_face_back(image, result_faces, masks, matrix)
        return PIL.Image.fromarray(img_result)
