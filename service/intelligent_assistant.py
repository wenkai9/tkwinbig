from db.polardb import PolarDB
from intelligent_assistant.qwen_assistant import QwenAssistant
from utils.conf import Conf


class IntelligentAssistant:
    def __init__(self, conf):
        self.qwen = QwenAssistant(conf)

    def chat(self, sessionid, user, content):
        return self.qwen.chat(sessionid=sessionid, user=user, content=content)

if __name__ == "__main__":
    conf = Conf().conf_parse("../conf/conf.yaml")
    ia = IntelligentAssistant(conf)
    creator = "max_test"
    content = "hello"
    # 与creator的第一次对话，content为空即可，和该creator的第二次对话时正常对话内容
    # 对话中，会将内容记录至数据库，与每个creator的对话都有一个session标识
    # 例如：
    # creator（实际为商家）：""
    # chabot："#商家的带货要约内容#"
    # creator（实际为达人）："i want more reward"
    # chabot："正常回复内容"
    resp_content, _, _ = ia.chat(sessionid="test_"+creator, user=creator, content=content)