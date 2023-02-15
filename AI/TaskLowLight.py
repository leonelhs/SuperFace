import PIL.Image
import numpy as np
import torch
import torch.optim
from torchvision.utils import make_grid

from AI.illuminate import model
from Tasks.TaskPhotoEnhancer import TaskPhotoEnhancer


class TaskLowLight(TaskPhotoEnhancer):

    def __init__(self, threadpool, progressBar, panel):
        super().__init__()
        self.threadpool = threadpool
        self.progressBar = progressBar
        self.panelOutput = panel
        self.DCE_net = model.enhance_net_nopool().cpu()
        device = torch.load('./models/snapshots/Epoch99.pth', map_location=torch.device('cpu'))
        self.DCE_net.load_state_dict(device)

    def logger(self, param, progress):
        pass

    def executeEnhanceWork(self, image, progress_callback):
        image = (np.asarray(image) / 255.0)
        image = torch.from_numpy(image).float()
        image = image.permute(2, 0, 1)
        image = image.cpu().unsqueeze(0)
        _, enhanced_image, _ = self.DCE_net(image)

        grid = make_grid(enhanced_image)
        ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to("cpu", torch.uint8).numpy()
        return PIL.Image.fromarray(ndarr)





