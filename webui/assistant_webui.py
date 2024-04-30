import gradio as gr

from intelligent_assistant.qwen_assistant import QwenAssistant

if __name__ == "__main__":
    qwen = QwenAssistant('')
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
        description="chat with the assistant of youwei"

    )
    ChatInterface.launch()