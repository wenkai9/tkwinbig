import gradio as gr
from dashscope.api_entities.dashscope_response import Role
from db.polardb import PolarDB
from intelligent_assistant.qwen_assistant import QwenAssistant
from utils.conf import Conf

if __name__ == "__main__":
    conf = Conf().conf_parse("../conf/conf.yaml")
    # polardb = PolarDB(conf["polardb"])
    # polardb.connect()
    # conf["dbconn"] = polardb
    qwen = QwenAssistant(conf)
    # output = qwen.chat("sessionid", "user", "hello")
    # print(output)
    def chat_func(input_text, creator, b_name, brand, p_info, link, reward, requirement, limits):
        # sessionid = "sellerid_creatorid_anchorid"
        sessionid = "id1_id2"
        sessionid = creator
        qwen.u_name = creator
        qwen.b_name = b_name
        qwen.brand = brand
        qwen.p_info = p_info
        qwen.link = link
        qwen.reward = reward
        qwen.requirement = requirement
        qwen.limits = limits
        output, history, system_prompt = qwen.chat_with_his(sessionid, Role.USER, input_text)
        # output = output['IntellgentAssistant Response']
        return output, history, system_prompt

    text1 = gr.Text(label="输入内容(content)", placeholder="与creator第一次对话时，不需要输入，直接submit即可，第二次对话时正常输入内容")
    text2 = gr.Text(label="达人ID(creator)", placeholder="达人ID(creator)", value="Maxim")
    text3 = gr.Text(label="商家名字(b_name)", placeholder="商家名字(b_name)", value="Vexloria")
    text4 = gr.Text(label="品牌(brand)", placeholder="品牌(brand)", value="Vexloria")
    text5 = gr.Text(label="商品信息(p_info)", placeholder="商品信息(p_info)", value="Vexloria -- a new brand focusing on 5 in 1 shaver")
    text6 = gr.Text(label="商品链接(link)", placeholder="商品链接(link)", value="https://shop.tiktok.com/view/product/1729401957854974731?region=US&locale=en")
    text7 = gr.Text(label="回报(reward)", placeholder="回报(reward)", value='''-Free Product
-20% Sales Commission
-Promote your video / send gifts in your live
    ''')
    text8 = gr.Text(label="要求(requirement)", placeholder="要求(requirement)", value='''-A 30 - 60 seconds video showing our product and post the video on your TikTok channel with our TikTok product link or put our link in your linktree.
-Do not forget to maintain your own creation style which is very important in making your content unique!
    ''')
    text9 = gr.Text(label="合作费上限(limits)", placeholder="合作费上限(limits)", value="200 dollars")


    output_text = gr.Textbox(label="最新回复")
    output_chatbot = gr.Chatbot(label="对话历史")
    ChatInterface = gr.Interface(
        fn=chat_func,
        inputs=[text1, text2, text3, text4, text5, text6, text7, text8, text9],
        outputs=[output_text, output_chatbot],
        title="IntelligentAssistant",
        description="An CBEC intelligent assistant, created by YWQC"

    )
    ChatInterface.launch()