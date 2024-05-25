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
        template = conf["template"]
        dashscope.api_key = qwen["dashscope"]["api_key"]
        self.model_name = qwen["model_name"]
        self.b_name = template["b_name"]
        self.brand = template["brand"]
        self.u_name = template["u_name"]
        self.p_info = template["p_info"]
        self.link = template["link"]
        self.reward = template["reward"]
        self.requirement = template["requirement"]
        self.limits = template["limits"]
        # self.dbconn = conf["dbconn"]
        self.tablename = 'tk_chat_record'
        # self.init_message()
        self.message = []

        # 初始化相关数据库
        self.polardb = PolarDB(conf["polardb"])
        self.db_init()

    def db_init(self):
        self.polardb.connect()

    # def init_message(self):
    #     user_init_message = AssistantConfig.USER_INIT_MESSAGE.format(b_name=self.b_name, brand=self.brand,
    #                                                                  u_name=self.u_name, p_info=self.p_info,
    #                                                                  link=self.link, reward=self.reward,
    #                                                                  requirement=self.requirement)
    #     self.message = []
    #     self.message.append(AssistantConfig.SYSTEM_INIT_MESSAGE)
    #     self.message.append({'role': 'user', 'content': user_init_message})

    def get_chat_his(self, sessionid, chat_type="DM"):
        result = self.polardb.select(table=self.tablename, condition={'sessionid': sessionid})
        # print(result)
        chat_his = []
        if len(result) == 0:
            # # 第一次对话，插入初始信息
            # sys_init_message = AssistantConfig.get_sys_init_message(chat_type=chat_type)
            sys_init_message = AssistantConfig.SYSTEM_INIT_MESSAGE_DM
            self.polardb.insert_tmp(table=self.tablename,
                               values=[{**{'sessionid':sessionid}, **sys_init_message}])
            chat_his.append(sys_init_message)
        else:
            # 非第一次对话，查询历史信息
            for r in result:
                # id, sessionid, role, content
                chat_his.append({'role': r[2], 'content': r[3]})
        return chat_his

    # sessionid: seller_creator_anchor
    def chat(self, sessionid, user, content, chat_type="DM"):
        print("request: {}".format({'role': user, 'content': content}))
        self.message = self.get_chat_his(sessionid)

        # 第一次访问，message中只有system_prompt内容，手动加入商家邀约信息
        if len(self.message) == 1:
            # 第一次对话，插入初始信息
            # user_init_message = AssistantConfig.get_user_init_message(chat_type=chat_type)
            user_init_message = AssistantConfig.USER_INIT_MESSAGE_DM
            user_init_message = user_init_message.format(b_name=self.b_name, brand=self.brand,
                                                               u_name=self.u_name, p_info=self.p_info,
                                                               link=self.link, reward=self.reward,
                                                               requirement=self.requirement, limits=self.limits)
            self.message.append({'role': 'user', 'content': user_init_message})

        # newest content
        if content == "":
            if len(self.message) > 2:
                return "***** empty input, no chat return *****"
            # # 第一次请求使用user init prompt msg
            content = self.message[1]["content"]
        else:
            print("request: {}".format({'role': user, 'content': content}))
            self.message.append({'role': user, 'content': content})
        print("mseeage length: {}".format(len(self.message)))

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
            self.polardb.insert_tmp(table=self.tablename,
                               values=[{'sessionid': sessionid, 'role': Role.USER, 'content': content},
                                     {'sessionid': sessionid, 'role': resp_role, 'content': resp_content}])
            return resp_content
        else:
            # print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            #     response.request_id, response.status_code,
            #     response.code, response.message
            # ))
            error_msg = str(response.request_id) + " " + str(response.status_code) + " " + str(response.code) + " " + response.message
            return error_msg

    def chat_with_his(self, sessionid, user, content, chat_type="DM"):
        print("request: {}".format({'role': user, 'content': content}))
        self.message = self.get_chat_his(sessionid)

        # 第一次访问，message中只有system_prompt内容，手动加入商家邀约信息
        if len(self.message) == 1:
            # 第一次对话，插入初始信息
            # user_init_message = AssistantConfig.get_user_init_message(chat_type=chat_type)
            user_init_message = AssistantConfig.USER_INIT_MESSAGE_DM
            user_init_message = user_init_message.format(b_name=self.b_name, brand=self.brand,
                                                               u_name=self.u_name, p_info=self.p_info,
                                                               link=self.link, reward=self.reward,
                                                               requirement=self.requirement, limits=self.limits)
            self.message.append({'role': 'user', 'content': user_init_message})

        # history content
        system_prompt = self.message[0]['content']
        his_list = []
        for msg in self.message[1:]:
            print(msg)
            msg_content = msg["content"]
            if msg['role'] == "user":
                his_list.append([msg_content])
            elif msg['role'] == "assistant":
                his_list[-1].append(msg_content)

        # newest content
        if content == "":
            if len(self.message) > 2:
                return "***** empty input, no chat return *****", his_list, system_prompt
            # # 第一次请求使用user init prompt msg
            content = self.message[1]["content"]
        else:
            print("request: {}".format({'role': user, 'content': content}))
            self.message.append({'role': user, 'content': content})
            his_list.append([content])
        print("mseeage length: {}".format(len(self.message)))

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
            self.polardb.insert_tmp(table=self.tablename,
                               values=[{'sessionid': sessionid, 'role': Role.USER, 'content': content},
                                     {'sessionid': sessionid, 'role': resp_role, 'content': resp_content}])
            his_list[-1].append(resp_content)
            return resp_content, his_list, system_prompt
        else:
            # print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            #     response.request_id, response.status_code,
            #     response.code, response.message
            # ))
            his_list[-1].append("chabot failed")
            error_msg = str(response.request_id) + " " + str(response.status_code) + " " + str(response.code) + " " + response.message
            return error_msg, his_list, system_prompt


import gradio as gr
if __name__ == "__main__":
    conf = Conf().conf_parse("../conf/conf.yaml")
    qwen = QwenAssistant(conf)
    # output = qwen.chat("sessionid", "user", "hello")
    # print(output)
    def chat_func(input_text, creator, history=[]):
        # sessionid = "sellerid_creatorid_anchorid"
        sessionid = "id1_id2"
        sessionid = creator
        output, history, system_prompt = qwen.chat(sessionid, Role.USER, input_text)
        # output = "你好"
        # output = output['IntellgentAssistant Response']
        return output, history, system_prompt

    '''
      model_name: qwen1.5-72b-chat
  b_name: Victoria
  brand: Vexloria
  u_name: Maxim
  p_info: Vexloria -- a new brand focusing on 5 in 1 shaver
  link: https://shop.tiktok.com/view/product/1729401957854974731?region=US&locale=en
  reward: 
  -Free Product
  -20% Sales Commission
  -Promote your video / send gifts in your live
  requirement: 
  -A 30 - 60 seconds video showing our product and post the video on your TikTok channel with our TikTok product link or put our link in your linktree.
  -Do not forget to maintain your own creation style which is very important in making your content unique!
    '''

    text1 = gr.Text(placeholder="content")
    text2 = gr.Text(placeholder="creator ", value="Maxim")
    text3 = gr.Text(placeholder="b_name", value="Vexloria")
    text3 = gr.Text(placeholder="brand", value="Vexloria")

    ChatInterface = gr.Interface(
        fn=chat_func,
        inputs=[text1, text2],
        outputs=["text"],
        title="IntelligentAssistant",
        description="chat with the chatbot@ss"

    )
    ChatInterface.launch()