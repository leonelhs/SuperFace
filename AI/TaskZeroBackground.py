import PIL
import cv2
import numpy as np
import torch
from PIL.Image import Image
from torchvision import transforms

from Tasks.TaskPhotoEnhancer import TaskPhotoEnhancer


def make_transparent_foreground(image, mask):
    # split the image into channels
    b, g, r = cv2.split(np.array(image).astype('uint8'))
    # add an alpha channel with and fill all with transparent pixels (max 255)
    a = np.ones(mask.shape, dtype='uint8') * 255
    # merge the alpha channel back
    alpha_im = cv2.merge([b, g, r, a], 4)
    # create a transparent background
    bg = np.zeros(alpha_im.shape)
    # set up the new mask
    new_mask = np.stack([mask, mask, mask, mask], axis=2)
    # copy only the foreground color pixels from the original image where mask is set
    foreground = np.where(new_mask, alpha_im, bg).astype(np.uint8)
    return foreground


def custom_background(background_file, foreground):
    final_foreground = Image.fromarray(foreground)
    background = Image.open(background_file)
    x = (background.size[0] - final_foreground.size[0]) / 2
    y = (background.size[1] - final_foreground.size[1]) / 2
    box = (x, y, final_foreground.size[0] + x, final_foreground.size[1] + y)
    crop = background.crop(box)
    final_image = crop.copy()
    # put the foreground in the centre of the background
    paste_box = (0, final_image.size[1] - final_foreground.size[1], final_image.size[0], final_image.size[1])
    final_image.paste(final_foreground, paste_box, mask=final_foreground)
    return final_image


class TaskZeroBackground(TaskPhotoEnhancer):

    def __init__(self, threadpool, progressBar, panel):
        super().__init__()
        self.threadpool = threadpool
        self.progressBar = progressBar
        self.panelOutput = panel
        self.model = torch.hub.load('pytorch/vision:v0.6.0', 'deeplabv3_resnet101', pretrained=True)
        self.model.eval()

    def logger(self, param, progress):
        pass

    def executeEnhanceWork(self, input_image, progress_callback):
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            self.model.to('cuda')

        with torch.no_grad():
            output = self.model(input_batch)['out'][0]
        output_predictions = output.argmax(0)

        # create a binary (black and white) mask of the profile foreground
        mask = output_predictions.byte().cpu().numpy()
        background = np.zeros(mask.shape)
        bin_mask = np.where(mask, 255, background).astype(np.uint8)

        foreground = make_transparent_foreground(input_image, bin_mask)

        return PIL.Image.fromarray(foreground)
