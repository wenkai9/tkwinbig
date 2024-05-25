import yaml


class Conf:
    def __init__(self):
        self.filename = 'conf.yaml'
        self.conf = None
        pass

    def conf_parse(self, filename):
        # 解析 YAML 文件
        with open(filename, 'r') as file:
            conf = yaml.safe_load(file)
        return conf