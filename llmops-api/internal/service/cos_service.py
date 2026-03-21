"""
@Time    : 2026/3/21
@Author  : chyu.wissfi@gmail.com
@File    : cos_service.py
"""
import os
import uuid
from datetime import datetime
from werkzeug.datastructures import FileStorage
import hashlib
from injector import inject
from dataclasses import dataclass
from qcloud_cos import CosS3Client, CosConfig
from internal.model import UploadFile
from internal.entity.upload_file_entity import ALLOWED_IMAGE_EXTENSION, ALLOWED_DOCUMENT_EXTENSION
from internal.exception import FailException
from .upload_file_service import UploadFileService


@inject
@dataclass
class CosService:
    """腾讯云cos服务"""
    upload_file_service: UploadFileService



    def upload_file(self, file: FileStorage, only_image: bool = False) -> UploadFile:
        """上传文件到腾讯云cos对象存储，上传后返回文件的信息"""
        # todo:等待授权认证模块完成进行切换调整
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"

        # 1. 提取文件扩展名并判断是否可以上传
        filename = file.filename
        extension = filename.split(".", 1)[-1] if "." in filename else ""
        
        if extension.lower() not in (ALLOWED_IMAGE_EXTENSION + ALLOWED_DOCUMENT_EXTENSION):
            raise FailException(f"该文件扩展名.{extension}扩展的文件不允许上传")
        elif only_image and extension.lower() not in ALLOWED_IMAGE_EXTENSION:
            raise FailException(f"该文件扩展名.{extension}扩展的文件不允许上传，请上传正确的图片")
        
        # 2. 获取客户端+存储桶名字
        client = self._get_client()
        bucket = self._get_bucket()

        # 3. 生成一个随机的名字
        random_name = f"{uuid.uuid4()}.{extension}"
        now = datetime.now()
        upload_filename = f"{now.year}/{now.month:02d}/{now.day:02d}/{random_name}"
        
        # 4.流式读取上传的数据并将其上传到cos中
        file_content = file.stream.read()

        try:
            # 5.将数据上传到cos存储桶中
            client.put_object(bucket, file_content, upload_filename)
        except Exception as e:
            raise FailException(f"上传文件到cos存储桶失败，请稍后重试，错误信息：{e}")

        # 6. 创建upload_file记录
        return self.upload_file_service.create_upload_file(
            account_id=account_id,
            name=filename,
            key=upload_filename,
            size=len(file_content),
            extension=extension,
            mime_type=file.mimetype,
            hash=hashlib.sha3_256(file_content).hexdigest(),
        )

    def download_file(self, key: str, target_file_path: str):
        """下载cos云端的文件到本地的指定路径"""
        client = self._get_client()
        bucket = self._get_bucket()

        client.download_file(bucket, key, target_file_path)


    @classmethod
    def get_file_url(cls, key: str) -> str:
        """根据传递的cos云端key获取文件的实际URL地址"""
        cos_domain = os.getenv("COS_DOMAIN")

        if not cos_domain:
            bucket = os.getenv("COS_BUCKET")
            scheme = os.getenv("COS_SCHEME")
            region = os.getenv("COS_REGION")
            cos_domain = f"{scheme}://{bucket}.cos.{region}.myqcloud.com"

        return f"{cos_domain}/{key}"

    @classmethod
    def _get_client(cls) -> CosS3Client:
        """获取cos客户端"""
        config = CosConfig(
            SecretId=os.getenv("COS_SECRET_ID"),
            SecretKey=os.getenv("COS_SECRET_KEY"),
            Region=os.getenv("COS_REGION"),
            Token=None,
            Scheme=os.getenv("COS_SCHEME", "https"),
        )
        return CosS3Client(config)

    @classmethod
    def _get_bucket(cls) -> str:
        """获取cos桶名字"""
        return os.getenv("COS_BUCKET")