"""
下载圣经
http://audio2.abiblica.org/bibles/app/audio/4_1.zip
...
http://audio2.abiblica.org/bibles/app/audio/4_66.zip
"""


import pathlib
from src.py.utils.log_util import default_logger as logger
from src.py.utils.constants import CONFIG_FILE, DATA_DIR
from src.py.utils.file_util import get_file_lines,save_config,load_config,check_zip_file


def download_single_file(url:str,download_filepath:pathlib.Path):
    """
    下载单个文件
    """
    logger.info(f"开始下载文件: {download_filepath}")
    download_filepath.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"下载文件完成: {download_filepath}")
    return check_zip_file(download_filepath)

def download_audios():
    """
    下载文件
    """
    logger.info(f"开始下载音频文件")
    config = load_config()
    for audio in config["bible"]["audio_list"]:
        if not audio["download_status"]:
            logger.info(f"文件未下载: {audio['download_filepath']}")
            if download_single_file(audio["url"],audio["download_filepath"]):
                audio["download_status"] = True
            else:
                audio["download_status"] = False
    save_config(config)
    logger.info(f"下载音频文件完成")

def check_download_status():
    """
    检查文件是否存在
    """
    logger.info("开始检查下载文件是否完整")
    config = load_config()
    for audio in config["bible"]["audio_list"]:
        if check_zip_file(audio["download_filepath"]):
            logger.info(f"文件完整: {audio['download_filepath']}")
            audio["download_status"] = True
        else:
            logger.info(f"文件不完整: {audio['download_filepath']}")
            audio["download_status"] = False
    save_config(config)
    logger.info("检查下载文件是否完整完成")

def generate_config():
    logger.info("开始生成配置文件")
    download_dir = DATA_DIR / "audio" / "download"
    config = {
        "bible": {
            "audio_list": [
                {
                    "url": "http://audio2.abiblica.org/bibles/app/audio/4_1.zip",
                    "output_dir": download_dir / "4_1",
                    "download_filepath": download_dir / "4_1.zip",
                    "bookname": "创世记",
                    "order": 1,
                    "category": "旧约",
                    "download_status": False,
                }
            ]
        }
    }
    (download_dir / "4_1").mkdir(parents=True, exist_ok=True)
    category_split_index = 40
    book_name_list = get_file_lines(DATA_DIR / "text" / "book_name_list.txt")
    for i in range(2, 67):
        if i < category_split_index:
            category = "旧约"
        else:
            category = "新约"

        config["bible"]["audio_list"].append(
            {
                "url": f"http://audio2.abiblica.org/bibles/app/audio/4_{i}.zip",
                "output_dir": download_dir / f"4_{i}",
                "download_filepath": download_dir / f"4_{i}.zip",
                "bookname": book_name_list[i - 1].strip(),
                "order": i,
                "category": category,
                "download_status": False,
            }
        )
        logger.info(f"开始创建目录: {download_dir/f'4_{i}'}")
        (download_dir / f"4_{i}").mkdir(parents=True, exist_ok=True)
    save_config(config)
    logger.info("配置文件生成完成")


if __name__ == "__main__":
    generate_config()
