import base64
import os
import tempfile
import uuid

import uvicorn
from fastapi import FastAPI
from paddleocr import PaddleOCR
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# 跨域问题处理
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageData(BaseModel):
    base64_image: str


# 模型目录
rec_model_dir = "./models/rec"
det_model_dir = "./models/det"
cls_model_dir = "./models/cls"

ocr = PaddleOCR(use_angle_cls=True, lang="ch", det_model_dir=det_model_dir,
                rec_model_dir=rec_model_dir,
                cls_model_dir=cls_model_dir)


def getOcrResult(img_path) -> list:
    """
    ocr识别结果
    :param img_path:
    :return:
    """
    result = ocr.ocr(img_path, cls=True)
    result_tests = []
    for idx in range(len(result)):
        try:
            res = result[idx]
            for line in res:
                result_tests.append(line[1][0])
        finally:
            continue

    return result_tests


@app.get("/")
def index():
    return "Hello, OCR!"


@app.post("/api/v1/convert_image")
def convert_image(image_data: ImageData):
    """
    识别图片中的文字
    :param image_data:
    :return:
    """
    try:
        # 解码base64图片数据
        image_bytes = base64.b64decode(image_data.base64_image)

        # 创建临时目录
        temp_dir = tempfile.gettempdir()

        # 生成唯一的文件名
        file_name = f"{uuid.uuid4()}.png"
        file_path = os.path.join(temp_dir, file_name)

        # 将图片数据写入临时文件
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        ocr_result = getOcrResult(file_path)
        return {
            "data": ocr_result,
            "code": 0,
            "msg": "success"
        }

    except Exception as e:
        return {
            "data": None,
            "code": 422,
            "msg": str(e)
        }


if __name__ == "__main__":
    try:
        import uvloop
    except ImportError:
        uvloop = None
    if uvloop:
        uvloop.install()

    # 启动服务
    uvicorn.run("main:app", host="0.0.0.0", port=9880, workers=1, reload=True)
