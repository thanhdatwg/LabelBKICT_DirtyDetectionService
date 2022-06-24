import cv2, json, os
from PIL import Image
import numpy
import torch
from src.utils.constants import FULL_PATH_IMAGE_FOLDER

def preprocess(path):
    image = Image.open(path)
    image = image.resize((1280, 960), Image.NEAREST)
    image = numpy.asarray(image).astype('uint8')

    x = torch.from_numpy(image).to("cpu").unsqueeze(0)
    x = torch.transpose(x, 3, 1) / 255

    return x.float()


def post_process(mask):
    mask = mask.squeeze().cpu().round()
    mask = torch.transpose(mask, 1, 0)

    return mask


def infer(model, path):
    x = preprocess(path)
    pr_mask = model.predict(x)
    mask = post_process(pr_mask)

    return mask


def ratio_element_matrix(x):
    h, w = x.shape
    sum_value = torch.sum(torch.FloatTensor(x))
    ratio = sum_value / (h*w)

    return ratio.item()

def get_path_image_file(message_value):
    if not message_value['image']:
        raise KeyError('Kafka message_value not key image')
    if not message_value['image']['originalImageFilename']:
        raise KeyError(
            'Kafka message_value image has null originalImageFilename')

    org_file_name = message_value['image']['originalImageFilename']
    full_path = os.path.join(FULL_PATH_IMAGE_FOLDER, org_file_name)
    return full_path
