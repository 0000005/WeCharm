import os

def get_data_dir():
    """获取数据目录的路径，并确保目录存在"""
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_file_path(filename):
    """获取指定文件在data目录下的完整路径"""
    data_dir = get_data_dir()
    return os.path.join(data_dir, filename)
