import cv2
import os


def prepare_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    else:
        # remove all files in the directory
        for file in os.listdir(dir_name):
            os.remove(f'{dir_name}/{file}')
    return dir_name


def draw_text(img,
              text,
              font=cv2.FONT_ITALIC,
              pos=(0, 0),
              font_scale=1,
              font_thickness=2,
              text_color=(255, 255, 255),
              text_color_bg=(0, 255, 0),
              padding=4
              ):
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size

    x, y = pos
    if y < text_h:
        y = y + text_h + padding

    cv2.rectangle(img, (x, y), (x + text_w + padding, y - text_h - 2 * padding), text_color_bg, -1)
    cv2.putText(img, text, (x, y + font_scale - 1), font, font_scale, text_color, font_thickness)


def draw_label(img, label, color=(12, 25, 255), border=2):
    c, x1, y1, x2, y2, conf = label
    cv2.rectangle(img, (x1, y1), (x2, y2), color, border)
    draw_text(img, f'{c}', pos=(x1 - border, y1), text_color_bg=color, padding=border)
