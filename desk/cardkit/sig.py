"""把島主手寫簽名的照片，轉成抓周卡用的落款圖：python3 sig.py 照片.jpg → signature.png（白色＝墨水，去背、裁邊）"""
import sys, numpy as np
from PIL import Image, ImageFilter, ImageOps
src = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else __file__.rsplit('/', 1)[0] + '/signature.png'
im = ImageOps.exif_transpose(Image.open(src)).convert('L')
im.thumbnail((2400, 2400))
a = np.asarray(im, dtype=float)
bg = np.asarray(im.filter(ImageFilter.GaussianBlur(40)), dtype=float)  # 紙張亮度（抵銷陰影）
ink = np.clip((bg - a) / np.maximum(bg, 1) * 3.0 - 0.15, 0, 1)        # 比紙暗的地方＝墨水
m = Image.fromarray((ink * 255).astype('uint8')).filter(ImageFilter.MedianFilter(3))
box = m.point(lambda v: 255 if v > 60 else 0).getbbox()
if not box: sys.exit('照片裡找不到簽名筆跡')
pad = 12; box = (max(0, box[0]-pad), max(0, box[1]-pad), min(m.width, box[2]+pad), min(m.height, box[3]+pad))
m.crop(box).save(out); print('已存成', out, m.crop(box).size)
