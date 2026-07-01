import yaml
import os

class YamlLoader:
    @staticmethod
    def load_data(file_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"数据文件不存在: {full_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data or []

    @classmethod
    def get_config(cls):
        """获取全局配置"""
        config_path = "config/config.yaml"
        return cls.load_data(config_path)