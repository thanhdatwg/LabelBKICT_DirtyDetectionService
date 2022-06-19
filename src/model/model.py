import torch
from src.model.utils import infer, ratio_element_matrix


class SegmentPolyp:
    def __init__(self, model_path) -> None:
        self.model_path = model_path
        self.torch_device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = torch.load(
            self.model_path, map_location=self.torch_device)

    def infer_file(self, path_file):
        mask = infer(self.model, path_file)
        return mask

    def ratio_mask_file(self, path_file):
        mask = self.infer_file(path_file)
        ratio_mask = ratio_element_matrix(mask)
        return ratio_mask
