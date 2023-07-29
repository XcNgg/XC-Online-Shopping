from aip import AipImageCensor # pip install baidu-aip
from PIL import Image
import os
from config import APP_ID,API_KEY,SECRET_KEY

CLIENT = AipImageCensor(APP_ID,API_KEY,SECRET_KEY)

def get_img_result(img_path):
    with open(img_path, 'rb') as i:
        #  获取img的编码信息
        imginfo = i.read()
    result = CLIENT.imageCensorUserDefined(imginfo)  # 调用接口审核信息
    return result



def convert_to_jpg(image_path):
    # 获取图像文件名和所在目录
    image_dir, image_filename = os.path.split(image_path)
    # 构建输出文件的完整路径
    output_path = os.path.join(image_dir, os.path.splitext(image_filename)[0] + ".jpg")
    # 打开图像并转换为RGB模式
    image = Image.open(image_path)
    rgb_image = image.convert("RGB")
    # 保存为JPG格式
    rgb_image.save(output_path, "JPEG")
    # 删除源文件
    os.remove(image_path)
    print(image_path+"--->"+output_path)
    return output_path


