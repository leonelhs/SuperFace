# Package methods

import cv2
import numpy as np

# Colors for all 20 parts
part_colors_a = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 0, 85], [255, 0, 170],
                 [0, 255, 0], [85, 255, 0], [170, 255, 0], [0, 255, 85], [0, 255, 170],
                 [0, 0, 255], [85, 0, 255], [170, 0, 255], [0, 85, 255], [0, 170, 255],
                 [255, 255, 0], [255, 255, 85], [255, 255, 170], [255, 0, 255], [255, 85, 255],
                 [255, 170, 255], [0, 255, 255], [85, 255, 255], [170, 255, 255]]

part_colors_b = [[0, 0, 0], [31, 119, 180], [44, 160, 44], [44, 127, 125], [52, 225, 143],
                 [217, 222, 163], [254, 128, 37], [130, 162, 128], [121, 7, 166], [136, 183, 248],
                 [85, 1, 76], [22, 23, 62], [159, 50, 15], [101, 93, 152], [252, 229, 92],
                 [167, 173, 17], [218, 252, 252], [238, 126, 197], [116, 157, 140], [214, 220, 252]]

part_colors = part_colors_b
colormap = np.array(part_colors, dtype=np.uint8)


def decode_segmentation_masks(mask, n_classes=20):
    red = np.zeros_like(mask).astype(np.uint8)
    green = np.zeros_like(mask).astype(np.uint8)
    blue = np.zeros_like(mask).astype(np.uint8)
    for chanel in range(0, n_classes):
        idx = mask == chanel
        red[idx] = colormap[chanel, 0]
        green[idx] = colormap[chanel, 1]
        blue[idx] = colormap[chanel, 2]
    return np.stack([red, green, blue], axis=2)


def vis_parsing_maps(image: np.array, parsing_anno, stride=1):
    image = np.array(image)
    vis_im = image.copy().astype(np.uint8)
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
