from PIL import Image
from PIL import ImageStat
from os import listdir
import tkinter

def amalgamate(base_path, dir_path=None, box_size=100):

    base_img = Image.open(base_path)
    if base_img.mode != 'RGBA':
        base_img = base_img.convert('RGBA')

    w, h = base_img.size
    w = (w // 100) * 100
    h = (h // 100) * 100

    root = tkinter.Tk()
    max_width = root.winfo_screenwidth()
    max_height = root.winfo_screenheight()
    root.destroy()

    if w > max_width or h > max_height:
        w = 1400
        h = 900
        w = (w // 100) * 100
        h = (h // 100) * 100

    base_img = base_img.resize((w, h))

    new_img = Image.new('RGBA', (w, h))
    mask_alpha = 150
    pics_required = (w // box_size) * (h // box_size)
    img_arr = [[0 for i in range((w // box_size))] for j in range((h // box_size))]
    img_arr_files = [[0 for i in range((w // box_size))] for j in range((h // box_size))]

    if dir_path:
        image_list = listdir(dir_path)
        index = 0

    row = 0
    for x in range((w // box_size)):
        x_off = x * box_size
        col = 0
        for y in range((h // box_size)):
            y_off = y * box_size
            box = (x_off, y_off, x_off + box_size, y_off + box_size)
            window = base_img.crop(box)

            stats = ImageStat.Stat(window).mean
            mean = tuple(map(int, stats[:3])) + (mask_alpha,)

            mask = Image.new('RGBA', (box_size, box_size), mean)
            file = ""

            if not dir_path:
                base = base_img.copy()
                base = base.resize((box_size, box_size))
            else:
                try:
                    file = dir_path + image_list[index]
                    base = Image.open(dir_path + image_list[index])
                    base = base.resize((box_size, box_size))
                    base = base.convert('RGBA')
                    index += 1
                except:
                    index += 1
                    if index == len(image_list):
                        index = 0
                    continue

                if index == len(image_list):
                    index = 0

            comp = Image.alpha_composite(base, mask)
            img_arr[col][row] = comp
            img_arr_files[col][row] = file
            new_img.paste(comp, box)

            col += 1
        row += 1
    return new_img, img_arr, img_arr_files