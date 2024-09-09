# 百度OCR本地模型版本接口
基于百度飞浆模型进行ocr识别的API接口服务, 默认集成的是cpu版本, 如有显卡需自行切换gpt版本

## 如何使用?

### 安装PaddlePaddle
- 您的机器安装的是CUDA 11，请运行以下命令安装
```bash
# cuda > 11.4
pip install paddlepaddle-gpu

# cuda > 11 <= 11.4
pip install paddlepaddle-gpu==2.5.0
```

- 您的机器是CPU，请运行以下命令安装
```bash
pip install paddlepaddle
```

- 安装其他所需依赖
```bash
pip install -r requirements.txt
```

### 接口请求
```curl
curl --location --request POST 'http://127.0.0.1:9880/api/v1/convert_image' \
--header 'User-Agent: Apifox/1.0.0 (https://apifox.com)' \
--header 'Content-Type: application/json' \
--data-raw '{
    "base64_image": "7EJCRAgQIAAAQIECBAgQIAAAQIECBAgQIBAnMAfNAlIoP+qICgAAAAASUVORK5CYII=...."
}'
```

## Docker 部署

> 默认的Docker镜像使用的是cpu版本, 如需使用gpu版本请自行修改Dockerfile

```bash
docker-compose up -d
```