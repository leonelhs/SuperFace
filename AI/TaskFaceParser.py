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
import torch
import torchvision.transforms as transforms
from PIL import Image

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer
from .faceparser.model import BiSeNet


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


model_path = './models/faceparser/79999_iter.pth'


class TaskFaceParser(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.net = BiSeNet(n_classes=19)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net.load_state_dict(torch.load(model_path, map_location=device))
        self.net.eval()

        self.to_tensor = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])

    def parseFace(self, image):
        with torch.no_grad():
            image = image.resize((512, 512), Image.BILINEAR)
            img = self.to_tensor(image)
            img = torch.unsqueeze(img, 0)
            if torch.cuda.is_available():
                img = img.cuda()
            out = self.net(img)[0]
            parsing = out.squeeze(0).cpu().numpy().argmax(0)
            dark_mask, color_mask = vis_parsing_maps(image, parsing)
            return parsing, dark_mask, color_mask

    def executeEnhanceWork(self, image, progress_callback):
        parsing, dark_mask, color_mask = self.parseFace(image)
        return PIL.Image.fromarray(color_mask)
