import gradio as gr
from dashscope.api_entities.dashscope_response import Role
from db.polardb import PolarDB
from intelligent_assistant.qwen_assistant import QwenAssistant
from utils.conf import Conf

if __name__ == "__main__":
    conf = Conf().conf_parse("../conf/conf.yaml")
    polardb = PolarDB()
    polardb.connect(host=conf["polardb"]["host"],
                    port=conf["polardb"]["port"],
                    user=conf["polardb"]["user"],
                    password=conf["polardb"]["password"],
                    database=conf["polardb"]["database"])
    conf["dbconn"] = polardb
    qwen = QwenAssistant(conf)
    # output = qwen.chat("sessionid", "user", "hello")
    # print(output)
    def chat_func(input_text, history=[]):
        # sessionid = "sellerid_creatorid_anchorid"
        sessionid = "id1_id2"
        output = qwen.chat(sessionid, Role.USER, input_text)
        # output = "你好"
        # output = output['IntellgentAssistant Response']
        return output

    ChatInterface = gr.Interface(
        fn=chat_func,
        inputs="text",
        outputs=["text"],
        title="IntelligentAssistant",
        description="chat with the chatbot@ss"

    )
    ChatInterface.launch()