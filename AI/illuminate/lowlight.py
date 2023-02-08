import os
import time

import numpy as np
import torch
import torch.optim
import torchvision
from PIL import Image

from AI.illuminate import model


def lowlight(image_path):
    data_lowlight = Image.open(image_path)
    data_lowlight = (np.asarray(data_lowlight) / 255.0)
    data_lowlight = torch.from_numpy(data_lowlight).float()
    data_lowlight = data_lowlight.permute(2, 0, 1)
    data_lowlight = data_lowlight.cpu().unsqueeze(0)

    DCE_net = model.enhance_net_nopool().cpu()
    device = torch.load('../../models/snapshots/Epoch99.pth', map_location=torch.device('cpu'))
    DCE_net.load_state_dict(device)
    start = time.time()
    _, enhanced_image, _ = DCE_net(data_lowlight)
    end_time = (time.time() - start)
    print(end_time)

    save_image_to = os.path.splitext(image_path)[0] + '-light.png'
    torchvision.utils.save_image(enhanced_image, save_image_to)
    return save_image_to
