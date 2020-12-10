# -*- coding: utf-8 -*-

'''
Created on 2020/12/10  14:26

@project: OCR

@filename: watermark.py

@author: zhangliang

@Desc:    
    
'''
import math
from PIL import Image, ImageDraw, ImageFont

#拼接图片
def image_compose(width_num,height_num,mark_img_path,mark_img_width,mark_img_height):
    compose_img_path = 'images/compose_img.png'
    to_image = Image.new('RGBA', (width_num * mark_img_width, height_num * mark_img_height)) #创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, height_num + 1):
        for x in range(1, width_num + 1):
            from_image = Image.open(mark_img_path).resize((mark_img_width,mark_img_height),Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * mark_img_width, (y - 1) * mark_img_height))
    # to_image.save(compose_img_path) # 保存新图
    return  to_image


#叠加图片
# 该接口使用掩码（mask）的形式对两幅图像进行合并。
def blend_images(src_img,compose_img,res_img_path):
    img1 = src_img

    img2 = compose_img

    r, g, b, alpha = img2.split()
    alpha = alpha.point(lambda i: i > 0 and 204)  # 204起到的效果和使用blend()接口时的0.3类似。

    img = Image.composite(img2, img1, alpha)

    img.show()
    img.save(res_img_path)

#添加水印
def add_water_mark(src_img_path,mark_img_path,res_img_path):
    src_img=Image.open(src_img_path)
    src_img = src_img.convert('RGBA')
    src_img_width,src_img_height=src_img.size

    #print('src_img_width=',src_img_width)
    #print('src_img_height=',src_img_height)

    mark_img = Image.open(mark_img_path)
    mark_img_width, mark_img_height = mark_img.size
    #print('mark_img_width=', mark_img_width)
    #print('mark_img_height=', mark_img_height)

    width_num=math.ceil(src_img_width / mark_img_width)
    height_num = math.ceil(src_img_height / mark_img_height)

    #拼接图片
    compose_img=image_compose(width_num, height_num, mark_img_path, mark_img_width, mark_img_height)
    #叠加图片
    blend_images(src_img,compose_img,res_img_path)

if __name__ == '__main__':
    src_img='images/sfz.png'
    mark_img='images/mark.png'
    res_img='images/sfz_mark.png'
    add_water_mark(src_img, mark_img, res_img)