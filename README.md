# litparse-rapidocr

基于 [LitServe](https://github.com/Lightning-AI/litserve) 和 [RapidOCR](https://github.com/RapidAI/RapidOCR) 的高性能 OCR 推理服务，为 [LitParse](https://github.com/run-llama/liteparse) 提供文档文字识别能力。

## 技术栈

| 组件 | 用途 |
|------|------|
| **LitServe** | AI 模型服务引擎，提供高性能 HTTP API |
| **RapidOCR** | 基于 ONNX Runtime 的轻量级 OCR 引擎 |
| **Pillow** | 图像加载与预处理 |
| **Pydantic** | 请求/响应数据结构验证 |
| **ONNX Runtime** | 跨平台 ML 推理加速 |
| **Uvicorn** | ASGI 服务器 |

## 快速开始

### 环境要求

- Python >= 3.12, <= 3.14

### 安装

```bash
uv sync
```

或手动安装依赖：

```bash
uv add litserve rapidocr pillow onnxruntime python-multipart uvicorn
```

### 启动服务

```bash
python server.py
```

服务默认运行在 `http://localhost:8000`，OCR 端点路径为 `/ocr`。

### API 说明

#### POST /ocr

上传图片进行 OCR 识别。

**请求参数**（`multipart/form-data`）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | file | ✅ | 待识别的图片文件 |
| `language` | string | ❌ | 识别语言，支持 `zh`/`chinese`（中文）、`en`/`english`（英文），默认 `zh` |

**响应格式**：

```json
{
  "results": [
    {
      "text": "识别出的文字",
      "bbox": [xmin, ymin, xmax, ymax],
      "confidence": 0.9876
    }
  ]
}
```

**示例调用**：

```bash
curl -X POST http://localhost:8000/ocr \
  -F "file=@document.png" \
  -F "language=zh"
```

```python
import requests

with open("document.png", "rb") as f:
    resp = requests.post(
        "http://localhost:8000/ocr",
        files={"file": f},
        data={"language": "en"}
    )
print(resp.json())
```

## 项目结构

```
litparse-rapidocr/
├── server.py          # 服务主入口（LitAPI 定义 + 启动逻辑）
├── pyproject.toml     # 项目配置与依赖声明
└── README.md
```

## 配置说明

`server.py` 中的关键配置：

- `api_path="/ocr"` — API 端点路径
- `workers_per_device=1` — 每个设备的 worker 数量，可根据 GPU/CPU 核心数调整
- `port=8000` — 服务端口

如需调整并发或性能，可修改 `LitServer` 的初始化参数，详见 [LitServe 文档](https://lightning.ai/docs/litserve)。 
