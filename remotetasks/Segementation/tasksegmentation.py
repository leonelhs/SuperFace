from abc import ABC
import numpy as np
import PIL.Image

from remotetasks.Segementation import vis_parsing_maps, decode_segmentation_masks
from remotetasks.remote_task import BaseRemoteTask
from toolset.BaseToolset import BaseToolset
from utils import uint8, makeImage


class TaskSegmentation(BaseRemoteTask, ABC):

    def __init__(self, parent: BaseToolset):
        super().__init__()
        self.files = dict()
        self.parent = parent

    def resource(self) -> str:
        return "segment"

    def runRemoteTask(self, image: bytes, port="5001"):
        self.files["image_a"] = image
        self.request(self.files, port)

    def onRequestResponse(self, reply):
        prediction_mask = np.asarray(reply)
        image = makeImage(self.files["image_a"])
        image = image.resize((512, 512), PIL.Image.BILINEAR)
        dark_map, overlay = vis_parsing_maps(image, prediction_mask)
        colormap = decode_segmentation_masks(dark_map)
        result = {"overlay": uint8(overlay), "colormap": uint8(colormap)}
        self.parent.onRequestResponse(self.resource(), result)

    def onRequestProgress(self, sent, total):
        self.parent.onRequestProgress(sent, total)

    def onRequestError(self, message, error):
        self.parent.onRequestError(message, error)
