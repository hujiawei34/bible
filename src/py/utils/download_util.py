"""
下载工具类
"""

import pathlib
import requests
from src.py.utils.log_util import default_logger as logger

def download_file(url: str, download_filepath: pathlib.Path):
    """
    下载文件
    """
    logger.info(f"开始下载文件: {download_filepath}")
    response = requests.get(url)
    with open(download_filepath, "wb") as f:
        f.write(response.content)
    logger.info(f"下载文件完成: {download_filepath}")
    return download_filepath
