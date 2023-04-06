import os
import shutil
import cv2

from tqdm import tqdm

RIDE = '1'

PATH = f'/home/janci/Documents/DIPLO/PILOT/{RIDE} David Brandys'


def process_labels():
    frames = dict()  # frame_id: [[object_id, x, y, x, y, conf], [...]]

    with open(f'{PATH}/labeled-video.txt', 'r') as f:
        labels = f.readlines()

        # reading the labels from file
        for label in tqdm(labels, desc=f"processing text file"):
            frame_id, cls, object_id, x1, y1, x2, y2, conf = label.strip().split(' ')

            frame_id = int(frame_id)

            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            if frame_id not in frames.keys():
                frames[frame_id] = []
            frames[frame_id].append([x1, y1, x2, y2])

        print(f'Frames ({len(frames.keys())}): {frames}')

    return frames


def main():
    # os read filenames in folder
    filenames = os.listdir(f'{PATH}/detected')
    filenames = [int(f.split('.')[0]) for f in filenames]

    frames = process_labels()
    frame_id = 0

    cap = cv2.VideoCapture(f'{PATH}/scenevideo-{RIDE}.mp4')

    while True:
        if frame_id % 500 == 0:
            print(frame_id)

        ret, frame = cap.read()

        if ret:

            if frame_id not in filenames:
                frame_id += 1
                continue

            with open(f'{PATH}/labels/{frame_id}.txt', 'a') as f:
                if frame_id in frames.keys():
                    for data in frames[frame_id]:
                        x1, y1, x2, y2 = data
                        # center of the bounding box
                        x = (x1 + x2) / 2
                        y = (y1 + y2) / 2
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)
                        x = x / 1920
                        y = y / 1080
                        w = w / 1920
                        h = h / 1080
                        x = float("{:.6f}".format(x))
                        y = float("{:.6f}".format(y))
                        w = float("{:.6f}".format(w))
                        h = float("{:.6f}".format(h))
                        f.write(f'Ad {x} {y} {w} {h}\n')

            cv2.imwrite(f'{PATH}/images/{frame_id}.jpg', frame)
            frame_id += 1
        else:
            break


def split_files_into_n_folders(n):
    # create n folders
    for i in range(n):
        os.mkdir(f'{PATH}/images/{i}')

    # split files into folders
    filenames = os.listdir(f'{PATH}/images')
    cut_length = len(filenames) // n
    next_cut = cut_length
    folder = 0
    for i, filename in enumerate(filenames):
        if i == next_cut:
            next_cut += cut_length
            folder += 1
        shutil.move(f'{PATH}/images/{filename}', f'{PATH}/images/{folder}/{filename}')


if __name__ == "__main__":
    # split_files_into_n_folders(20)
    main()
