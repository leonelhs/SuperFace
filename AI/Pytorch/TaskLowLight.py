#############################################################################
#
#   Source from:
#   https://github.com/Li-Chongyi/Zero-DCE/
#   Forked from:
#   https://github.com/Li-Chongyi/Zero-DCE/
#   Reimplemented by: Leonel Hernández
#
##############################################################################
import PIL.Image
import numpy as np
import torch
import torch.optim
from torchvision.utils import make_grid

from AI.illuminate import model
from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer

model_path = "./models/snapshots/Epoch99.pth"


class TaskLowLight(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.DCE_net = model.enhance_net_nopool().cpu()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        state = torch.load(model_path, map_location=device)
        self.DCE_net.load_state_dict(state)

    def executeEnhanceWork(self, image, progress_callback):
        image = (np.asarray(image) / 255.0)
        image = torch.from_numpy(image).float()
        image = image.permute(2, 0, 1)
        image = image.cpu().unsqueeze(0)
        _, enhanced_image, _ = self.DCE_net(image)

        grid = make_grid(enhanced_image)
        ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to("cpu", torch.uint8).numpy()
        return PIL.Image.fromarray(ndarr)
