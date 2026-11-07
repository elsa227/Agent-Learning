# 【功能说明】使用Gradio库创建一个简单的文本处理应用，包括文本倒序和字符数统计

#案例1 一个接收文本输入并返回该文本倒序输出的应用
import gradio as gr

#功能实现
# def reverse_text(text):
#     return text[::-1]

# def hellotoPerson(name):
#     return "你好，" + name

def reverse_and_count(text):
    reversed_text = text[::-1]
    length = len(text)
    return reversed_text, length

#界面配置
# demo = gr.Interface(
#     fn=hellotoPerson, #fn不能改，固定的函数名
#     inputs="text", 
#     outputs="text")

demo = gr.Interface(
    fn=reverse_and_count, #fn不能改，固定的函数名
    inputs="text", 
    outputs=["text", "number"],
    title = "文本处理工具",
    description = "输入文本，输出倒序文本和字符数",
    examples = [["你好 世界"],["Heloo World"]]
)

#运行应用
demo.launch()
#关闭应用
demo.close()