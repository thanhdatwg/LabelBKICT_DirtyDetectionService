import torch, json, os
from src.utils.handle import get_path_image_file, infer, ratio_element_matrix
from src.utils.constants import SEGMENT_POLYP_MODEL_PATH, POSTGRESQL_CONNECT, DIRTY_IMAGE_INDEX, DIRTY, CLEAN
from src.model.database import Database

postgresql_worker = Database(POSTGRESQL_CONNECT)

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
    
def get_ratio_result(message_value_formatted):
    segment_polyp = SegmentPolyp(SEGMENT_POLYP_MODEL_PATH)
    full_path_image = get_path_image_file(message_value_formatted)
    try:
        ratio_result = segment_polyp.ratio_mask_file(full_path_image)
        print(ratio_result)
        if ratio_result >= DIRTY_IMAGE_INDEX:
            result_status = DIRTY
            sql_query_update_ratio_result = f"INSERT INTO image_service_image_has_image_tag_tab (image_id, image_tag_id) VALUES ({message_value_formatted['image']['id']}, {result_status})"
            postgresql_worker.execute_query(sql_query_update_ratio_result)
        
    except Exception as e:
        print(e)
    
    
