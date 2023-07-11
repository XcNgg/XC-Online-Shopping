from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont
import base64

def generate_image():
    '''
    返回图片验证码信息
    :return:
    '''
    width, height, font_size, font_num = 300, 100, 60, 5
    bg_color = (255, 255, 255)
    image = Image.new(mode='RGB', size=(width, height), color=bg_color)  # 画布
    draw = ImageDraw.Draw(image, mode='RGB')  # 绘图类
    font = ImageFont.truetype("./static/fonts/AlimamaFangYuanTiVF-Thin.ttf", font_size)  # 字体
    verify = str()
    for i in range(font_num):
        x = random.randint(i * (width / font_num), (i + 1) * (width / font_num) - font_size)
        y = random.randint(0, height - font_size)
        char = random.choice([chr(alpha) for alpha in range(65, 91)] + [str(num) for num in range(10)])  # 随机参数拼接给verify
        verify += char
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.text((x, y), char, fill=color, font=font)
    by = BytesIO()
    image.save(by, format='PNG')
    image_byte = by.getvalue()
    image_base64 = convert_image_to_base64(image_byte)
    # 返回验证码和转换后的base64图像
    return verify, image_base64


def convert_image_to_base64(image_byte):
    """
    将图像转换为Base64字符串
    :param image_byte: 图像的字节数据
    :return: Base64字符串
    """
    image_base64 = base64.b64encode(image_byte).decode('utf-8')
    return image_base64
