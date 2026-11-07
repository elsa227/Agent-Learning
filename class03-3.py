# 【功能说明】创建一个简单的Deepseek模型调用应用，支持与Deepseek模型进行对话

import gradio as gr
import os  #用于访问环境变量
from openai import OpenAI  #OpenAI 兼容API的客户端库，用于调用通义千问

#从系统环境变量中获取Dash Scope API密钥
#确保在运行此脚本前已设置DASHSCOPE_API_KEY环境变量
api_key = os.getenv("DASHSCOPE_API_KEY")

if not api_key:

def call_deepseek(message,history):
    """
    调用Deepseek模型，返回模型回复

    参数：
    message（str）：用户输入的消息
    history（list）：用户与模型的对话历史记录，支持两种格式：
                   格式1：{(用户消息，助手回复)，...}  -元组列表格式
                   格式2：[{"role": "user", "content": "用户消息"}, {"role": "assistant", "content": "助手回复"}]  -字典列表格式
    返回：
    str：模型回复的消息，如果发生错误则返回格式化的错误信息

    功能说明:
        1.验证API密钥是否存在，确保服务可用性
        2.创建OpenAI客户端，配置Deepseek的兼容模式API端点
        3.构建包含历史对话和当前消息的完整消息列表，维护对话上下文
        4.处理不同格式的历史消息，确保兼容性
        5.调用Deepseek模型deepseek-max生成回复
        6.捕获并处理可能的异常，返回友好的错误信息

    错误处理:
        API密钥不存在:返回错误提示，指导用户设置环境变量
        历史记录格式错误:尝试多种格式解析，出错时记录日志但不中断执行
        API调用失败:返回原始错误信息，便于调试
    """

if not api_key:
    return "错误，未设置DASHSCOPE_API_KEY环境变量，请设置后重试。"

#初始化OpenAI客户端，配置Deepseek的兼容模式API端点
#这个初始化步骤配置了API密钥和基础URL，使得我们可以通过标准OpenAI接口调用Deepseek的服务
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.cn/v1"
    )

#构建消息列表，用于维持对话上下文
#这个列表将被传递给模型，包含完整的对话历史和当前信息
messages = []

if history:
    #遍历历史记录，正确处理给gradio chatinterface的消息格式
    #这里加了异常处理，确保即使历史记录不正确也不会导致程序崩溃
    try:
        #尝试处理字典格式的history（较新版本Gradio的格式）
        for msg in history:
            #检查是否为字典格式且包含必要的role和content字段
            if isinstance(msg,dict) and 'role' in msg and 'content' in msg:
                messages.append(msg)
            #检查是否为元组或列表格式（较旧版本的gradio格式）
            elif isinstance(msg,(list,tuple)) and len(msg) == 2:
                messages.append({"role":"user","content":user_msg})
                messages.append({"role":"assistant","content":assistant_msg})
    except Exception as e:
        print(f"处理历史记录时出错：{e}")

messages.append({"role":"user","content":message})#每次把上一次的历史数据+用户数据返回到用户数据，保持对话上下文连续


try:
    response = client.chat.completetions.create(
        model = "deepseek-max",
        messages = messages,
        stream=False   #设置为飞流式响应（一次性返回完整结果）
    )

    #提取并返回模型生成的内容
    return response.choices[0].message.content

except Exception as e:
    return "Error:" + str(e)

demo = gr.Interface(
    fn=call_deepseek, 
    fn = call_deepseek
    title="Deepseek Chat",
    description="与Deepseek模型进行对话",
    examples=[
        ["你好"],
        ["你叫什么名字？"],
        [给我讲一个笑话""]
    ]
)


if __name__ == "__main__":
    demo.launch(thenme=gr.themes.Soft())