import cv2
from PIL import Image
import numpy
import torch


def preprocess(path):
    image = Image.open(path)
    image = image.resize((1280, 960), Image.NEAREST)
    image = numpy.asarray(image).astype('uint8')

    x = torch.from_numpy(image).to("cpu").unsqueeze(0)
    x = torch.transpose(x, 3, 1) / 255

    return x.float()


def postprocess(mask):
    mask = mask.squeeze().cpu().round()
    mask = torch.transpose(mask, 1, 0)

    return mask


def infer(model, path):
    x = preprocess(path)
    pr_mask = model.predict(x)
    mask = postprocess(pr_mask)

    return mask


def ratio_element_matrix(x):
    h, w = x.shape
    sum_value = torch.sum(torch.FloatTensor(x))
    ratio = sum_value / (h*w)

    return ratio.item()
