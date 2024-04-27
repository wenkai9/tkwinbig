from typing import List, Dict

import dashscope
import random
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from dev.intelligent_assistant.assistant_interface import AssistantInterface
from dev.conf.assistant_config import AssistantConfig
from dev.db.polardb import PolarDB
from http import HTTPStatus


class QwenAssistant(AssistantInterface):
    def __init__(self, dbconn):
        dashscope.api_key = "sk-eec49836751644339ce2b7488f63d9cb"
        self.b_name = 'Victoria'
        self.brand = 'Vexloria'
        self.u_name = 'Maxim'
        self.p_info = 'Vexloria -- a new brand focusing on 5 in 1 shaver'
        self.link = 'https://shop.tiktok.com/view/product/1729401957854974731?region=US&locale=en'
        self.reward = '''-Free Product
        -20% Sales Commission
        -Promote your video / send gifts in your live'''
        self.requirement = '''-A 30 - 60 seconds video showing our product and post the video on your TikTok channel with our TikTok product link or put our link in your linktree.
        -Do not forget to maintain your own creation style which is very important in making your content unique!'''
        self.model_name = 'qwen1.5-72b-chat'
        self.dbconn = dbconn
        self.tablename = 'tk_chat_record'
        self.init_message()

    def init_message(self):
        user_init_message = AssistantConfig.USER_INIT_MESSAGE.format(b_name=self.b_name, brand=self.brand,
                                                                     u_name=self.u_name, p_info=self.p_info,
                                                                     link=self.link, reward=self.reward,
                                                                     requirement=self.requirement)
        self.message = []
        self.message.append(AssistantConfig.SYSTEM_INIT_MESSAGE)
        self.message.append({'role': 'user', 'content': user_init_message})

    def get_chat_his(self, sessionid, user):
        result = self.dbconn.select(table=self.tablename, where={'user': user, 'sessionid': sessionid})
        chat_his = []
        if len(result) == 0:
            # 第一次对话，插入初始信息
            user_init_message = AssistantConfig.USER_INIT_MESSAGE.format(b_name=self.b_name, brand=self.brand,
                                                                         u_name=self.u_name, p_info=self.p_info,
                                                                         link=self.link, reward=self.reward,
                                                                         requirement=self.requirement)
            self.dbconn.insert(table=self.tablename, data={**AssistantConfig.SYSTEM_INIT_MESSAGE, **{'sessionid':sessionid}})
            self.dbconn.insert(table=self.tablename, data={'sessionid':sessionid, 'role': 'user', 'content': user_init_message})
            chat_his.append(AssistantConfig.SYSTEM_INIT_MESSAGE)
            chat_his.append({'role': 'user', 'content': user_init_message})
        else:
            # 非第一次对话，查询历史信息
            for r in result:
                chat_his.append({'role': r.role, 'content': r.content})
        return chat_his

    def chat(self, user, content):
        # self.message = self.dbconn.select(table='tk_chat_his', where={'user': user, 'sessionid': sessionid})
        self.message.append({'role': Role.USER, 'content': content})
        response = Generation.call(
            self.model_name,
            messages=self.message,
            seed=random.randint(1, 10000),
            result_format='message',
        )
        if response.status_code == HTTPStatus.OK:
            # print("机器人回应:", response.output.choices[0]['message']['content'])
            # self.dbconn.insert(table=self.tablename, data={'sessionid':sessionid, 'user': user, 'role': Role.USER, 'content': content})
            # self.dbconn.insert(table=self.tablename, data={'sessionid':sessionid, 'user': user,
            #                                               'role': response.output.choices[0]['message']['role'],
            #                                               'content': response.output.choices[0]['message']['content']})
            return {'IntellgentAssistant Response': response.output.choices[0]['message']['content']}
        else:
            # print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            #     response.request_id, response.status_code,
            #     response.code, response.message
            # ))
            return response.output.choices[0]['message']['content']

# if __name__ == "__main__":
#     # dashscope.api_key = "sk-eec49836751644339ce2b7488f63d9cb"
#     polardb = PolarDB()
#     polardb.connect(host='tkwinbig.rwlb.rds.aliyuncs.com', port = 3306,
#                     user='tkwinbig', password='tkwinbig@321', database='tkwinbig_test')
#     qwen = QwenAssistant(polardb)
#     qwen.chat("hello", "test_0")
#
#     polardb.close()
#     print(qwen.message)


import gradio as gr

if __name__ == "__main__":
    qwen = QwenAssistant('')

    def flatten(matrix: List[List[str]]) -> List[str]:
        flat_list = []
        for row in matrix:
            flat_list += row
        return flat_list

    def to_chat(lst: List[str]) -> List[Dict[str, str]]:
        res = []
        for i in range(len(lst)):
            role = "system" if i % 2 == 1 else "user"
            res.append({"role": role, "content": lst[i]})
        return res

    def chat_reply(input_text, history=[]):
        output = qwen.chat("user", input_text)
        # output = "你好"
        output = output['IntellgentAssistant Response']
        return output


    # ChatInterface = gr.ChatInterface(
    #     fn=chat_reply,
    #     title="IntelligentAssistant",
    #     description="chat with the chatbot"
    #
    # )

    ChatInterface = gr.Interface(
        fn=chat_reply,
        inputs="text",
        outputs=["text"],
        title="IntelligentAssistant",
        description="chat with the chatbot"

    )
    ChatInterface.launch()