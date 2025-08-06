"""
文件操作工具类
"""

import os
import json
import pathlib
import zipfile
from src.py.utils.constants import CONFIG_FILE
from src.py.utils.log_util import default_logger as logger

def load_config(config_file=CONFIG_FILE):
    logger.info(f"开始加载配置文件: {config_file}")
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config, config_file=CONFIG_FILE):
    logger.info(f"开始保存配置文件: {config_file}")
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False,cls=PathEncoder)

def read_file(file_path):
    logger.info(f"开始读取文件: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(file_path, content):
    logger.info(f"开始写入文件: {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def get_file_lines(file_path):
    logger.info(f"开始获取文件内容: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        line_list = f.readlines()
    logger.info(f"文件内容获取完成: {file_path},行数: {len(line_list)}")
    return line_list

class PathEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pathlib.Path):
            return str(obj)
        return super().default(obj)


def check_zip_file(file_path):
    """
    检查文件是否完整zip包
    """
    logger.info(f"开始检查文件是否完整zip包: {file_path}")
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    if not file_path.exists():
        logger.info(f"文件不存在: {file_path}")
        return False
    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            if len(zip_ref.namelist()) == 0:
                logger.info(f"文件为空: {file_path}")
                return False
            logger.info(f"文件完整: {file_path}")
            return True
    except zipfile.BadZipFile:
        logger.info(f"文件格式错误: {file_path}")
        return False
        