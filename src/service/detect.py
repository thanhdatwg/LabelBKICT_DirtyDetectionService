import torch, json, os
from src.utils.handle import get_path_image_file, infer, ratio_element_matrix
from src.utils.constants import SEGMENT_POLYP_MODEL_PATH, POSTGRESQL_CONNECT, STATUS
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
    
def get_ratio_result(message_value):
    segment_polyp = SegmentPolyp(SEGMENT_POLYP_MODEL_PATH)
    full_path_image = get_path_image_file(message_value)
    try:
        ratio_result = segment_polyp.ratio_mask_file(full_path_image)
        print(ratio_result)
        message_value_formatted = json.loads(message_value.decode("utf-8"))

        if ratio_result >= 0.8:
            result_status = STATUS.dirty
        else:
            result_status = STATUS.clean

        sql_query_update_ratio_result = f"UPDATE image_service_image_tab SET is_dirty = { result_status } where image_id =  {message_value_formatted['image']['id']} " 
        postgresql_worker.execute_query(sql_query_update_ratio_result)
    except Exception as e:
        print(e)
    
    
