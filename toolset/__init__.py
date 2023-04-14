import PIL
import cv2
import numpy as np

dataX3 = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
dataX5 = [[1, 1, 1, 1, 1],
          [1, 5, 5, 5, 1],
          [1, 5, 44, 5, 1],
          [1, 5, 5, 5, 1],
          [1, 1, 1, 1, 1]]


def ndArray(array):
    return np.uint8(array)


def floodFill(image, position, color):
    cv2.floodFill(image, None, position, color)


def bitWiseAnd(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)


def makeMask(image, color):
    return 255 - cv2.inRange(image, color, color)


def resize(image, size):
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def makeImage(array):
    return PIL.Image.fromarray(array)
