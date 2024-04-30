import sys
from typing import List, Dict

import dashscope
import random
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

from db.polardb import PolarDB
from intelligent_assistant.assistant_interface import AssistantInterface
from conf.assistant_config import AssistantConfig
from http import HTTPStatus
from utils.conf import Conf

class QwenAssistant(AssistantInterface):
    def __init__(self, conf):
        qwen = conf["qwen"]
        dashscope.api_key = qwen["dashscope"]["api_key"]
        self.b_name = qwen["b_name"]
        self.brand = qwen["brand"]
        self.u_name = qwen["u_name"]
        self.p_info = qwen["p_info"]
        self.link = qwen["link"]
        self.reward = qwen["reward"]
        self.requirement = qwen["requirement"]
        self.model_name = qwen["model_name"]
        self.dbconn = conf["dbconn"]
        self.tablename = 'tk_chat_record'
        # self.init_message()
        self.message = []

    def init_message(self):
        user_init_message = AssistantConfig.USER_INIT_MESSAGE.format(b_name=self.b_name, brand=self.brand,
                                                                     u_name=self.u_name, p_info=self.p_info,
                                                                     link=self.link, reward=self.reward,
                                                                     requirement=self.requirement)
        self.message = []
        self.message.append(AssistantConfig.SYSTEM_INIT_MESSAGE)
        self.message.append({'role': 'user', 'content': user_init_message})

    def get_chat_his(self, sessionid):
        result = self.dbconn.select(table=self.tablename, condition={'sessionid': sessionid})
        # print(result)
        chat_his = []
        if len(result) == 0:
            # 第一次对话，插入初始信息
            user_init_message = AssistantConfig.USER_INIT_MESSAGE.format(b_name=self.b_name, brand=self.brand,
                                                                         u_name=self.u_name, p_info=self.p_info,
                                                                         link=self.link, reward=self.reward,
                                                                         requirement=self.requirement)
            self.dbconn.insert(table=self.tablename,
                               values=[{**{'sessionid':sessionid}, **AssistantConfig.SYSTEM_INIT_MESSAGE},
                                     {'sessionid':sessionid, 'role': 'user', 'content': user_init_message}])
            chat_his.append(AssistantConfig.SYSTEM_INIT_MESSAGE)
            chat_his.append({'role': 'user', 'content': user_init_message})
        else:
            # 非第一次对话，查询历史信息
            for r in result:
                # id, sessionid, role, content
                chat_his.append({'role': r[2], 'content': r[3]})
        return chat_his

    # sessionid: seller_creator_anchor
    def chat(self, sessionid, user, content):
        self.message = self.get_chat_his(sessionid)
        self.message.append({'role': user, 'content': content})
        print("request: {}".format({'role': user, 'content': content}))
        response = Generation.call(
            self.model_name,
            messages=self.message,
            seed=random.randint(1, 10000),
            result_format='message',
        )
        print("response: {}".format(response))
        if response.status_code == HTTPStatus.OK:
            # print("机器人回应:", response.output.choices[0]['message']['content'])
            resp_role = response.output.choices[0]['message']['role']
            resp_content = response.output.choices[0]['message']['content']
            self.dbconn.insert(table=self.tablename,
                               values=[{'sessionid': sessionid, 'role': Role.USER, 'content': content},
                                     {'sessionid': sessionid, 'role': resp_role, 'content': resp_content}])
            return resp_content
        else:
            # print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            #     response.request_id, response.status_code,
            #     response.code, response.message
            # ))
            return str(response.request_id) + " " + str(response.status_code) + " " + str(response.code) + " " + response.message


import gradio as gr
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