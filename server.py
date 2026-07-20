import litserve as ls
from ocrapi import OcrAPI
if __name__ == "__main__":
    api = OcrAPI()
    server = ls.LitServer(api, api_path="/ocr",workers_per_device=1)  # 自定义端点路径
    server.run(port=8000)