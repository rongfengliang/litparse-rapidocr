import litserve as ls
import io
from PIL import Image
from rapidocr import  RapidOCR
from pydantic import BaseModel
from typing import Any

class OcrResponse(BaseModel):
    results: list[Any]

class OcrAPI(ls.LitAPI):
    def setup(self, device):
        self.engine = RapidOCR()
    def normalize_language(self, lang):
        # 模仿你示例中的规范化逻辑
        lang_map = {"en": "en", "english": "en", "zh": "zh", "chinese": "zh"}
        return lang_map.get(lang.lower(), "zh")  # 默认中文

    def decode_request(self, request):
        # 1. 获取上传的文件（字段名 "file"）
        file_obj = request["file"]
        contents = file_obj.file.read()
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")

        # 2. 获取语言参数（字段名 "language"，默认 "en"）
        lang = request.get("language", "zh")
        lang = self.normalize_language(lang)

        # 返回一个元组，供 predict 使用
        return pil_image, lang

    def predict(self, inputs):
        image, lang = inputs
        import time
        start_time = time.time()
        print("starting", time.time())
        result = self.engine(image)
        print(f"Performing OCR with language: {lang}")
        end_time = time.time()
        print("ending", end_time)
        print(f"OCR processing time: {end_time - start_time} seconds")
        final_result = []
        boxes = [] if result.boxes is None else result.boxes
        txts = [] if result.txts is None else result.txts
        scores = [] if result.scores is None else result.scores
        for box, text, score in zip(
                boxes,
                txts,
                scores,
            ):
            xs = [p[0] for p in box]
            ys = [p[1] for p in box]
            xmin = min(xs)
            ymin = min(ys)
            xmax = max(xs)
            ymax = max(ys)
            bbox = [float(xmin), float(ymin), float(xmax), float(ymax)]
            confidence = float(score)
            item = {"text": text, "bbox": bbox, "confidence": confidence}
            final_result.append(item)
        return OcrResponse(results=final_result)

if __name__ == "__main__":
    api = OcrAPI()
    server = ls.LitServer(api, api_path="/ocr",workers_per_device=1)  # 自定义端点路径
    server.run(port=8000)