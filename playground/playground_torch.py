import pickle

import PIL
import torch
import dnnlib
import torch_utils
from PIL import Image


with open('../../models/stylegan/stylegan2-celebahq-256x256.pkl', 'rb') as f:
    G = pickle.load(f)['G_ema'].cpu()  # torch.nn.Module
z = torch.randn([100, G.z_dim]).cpu()    # latent codes
c = None                                # class labels (not used in this example)
img = G(z, c)

# img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
img = PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB')

# display the PIL image
img.show()
