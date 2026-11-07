import cv2  # 导入 OpenCV 库，专门用来做图像处理（比如滤镜、模糊、边缘检测）
import numpy as np  # 导入 NumPy 库，它能把图片变成数字矩阵进行数学加减乘除（起个外号叫 np 方便打字）
import gradio as gr  # 导入 Gradio 库，用来一键生成网页界面（起个外号叫 gr）

def image_to_sketch(image):  # 定义一个函数叫 image_to_sketch，括号里的 image 就是用户在网页上上传的那张图
    gray_image = image.convert('L')  # 把彩色的 image 转换成灰度图（黑白图），'L' 代表 Luminance（亮度通道），这是最简单的转黑白方法
    inverted_image = 255 - np.array(gray_image)  # 反色处理（像底片）。np.array(gray_image) 把图片变成数字矩阵；数字 255 代表纯白色，用 255 减去原图的每一个像素，黑的就变白，白的变黑
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)  # 对反色后的图进行“高斯模糊”。(21, 21) 是模糊的窗口大小，相当于拿一个 21x21 像素的毛玻璃去平滑图像，数字越大越模糊；0 代表让系统自动计算模糊程度
    pencil_sketch = cv2.divide(np.array(gray_image), 255 - blurred, scale=256.0)  # 核心算法：颜色减淡。用原图的灰度矩阵，除以 (255 减去模糊图) 的矩阵。scale=256.0 是一个缩放比例，用来把计算结果拉伸回 0-255 的正常颜色范围
    return pencil_sketch  # 把最终计算出来的“素描图”数据丢出去，交给网页显示

demo = gr.Interface(  # 搭建网页界面（Interface 是接口的意思）
    fn=image_to_sketch,  # fn 代表 function（函数），告诉网页：用户点击按钮时，请执行上面那个 image_to_sketch 函数
    inputs=[gr.Image(label="上传图片", type="pil")],  # inputs 定义输入框：[ ] 表示列表，里面放了一个图片组件（Image）；label 是显示给用户看的标题；type="pil" 告诉系统接收 Python 的 PIL 图像格式
    outputs=[gr.Image(label="铅笔画")],  # outputs 定义输出框：同样放一个图片组件，用来展示我们处理完的素描图
    title="图像转铅笔画",  # 网页最顶端的大标题
    description="将上传的图片转换为铅笔画效果",  # 标题下面的一行小字说明
)  # 右括号闭合 gr.Interface

demo.launch()  # 启动网页！运行后，终端会弹出一个本地网址（如 http://127.0.0.1:7860），按住 Ctrl 点它就能在浏览器打开