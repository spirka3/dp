import os
import cv2

from tracking.utils import draw_label, prepare_dir


def process_frames(chunk_name):
    mot_frames = dict()

    with open(f'{src_dir}/tracker/tracks/{chunk_name}.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            frame, obj, left, top, width, height, conf, x, y, z = line.split()
            if frame not in mot_frames:
                mot_frames[frame] = []
            mot_frames[frame].append((obj, int(left), int(top), int(width), int(height), conf, x, y, z))

    return mot_frames


def read_video(chunk_name):
    mot_frames = process_frames(chunk_name)

    cap = cv2.VideoCapture(f'{src_dir}/tracker/{chunk_name}.mp4')
    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame_id = str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))

        if frame_id not in mot_frames:
            cv2.imwrite(f'{src_dir}/checker/{chunk_name}/none/{frame_id}.jpg', frame)
            continue

        for label in mot_frames[frame_id]:
            c, left, top, width, height, conf, x, y, z = label
            x1, y1, x2, y2 = left, top, left + width, top + height
            label = (c, x1, y1, x2, y2, conf)
            draw_label(frame, label, color=(12, 25, 255), border=2)

        cv2.imwrite(f'{src_dir}/checker/{chunk_name}/matched/{frame_id}.jpg', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    src_dir = 'ride-1'

    # create list of unique chunk names
    chunk_names = [x.split('.')[0] for x in os.listdir(f'{src_dir}/tracker/tracks')]

    for chunk_name in chunk_names:
        if chunk_name == 'chunks-1-0':
            continue
        prepare_dir(f'{src_dir}/checker/{chunk_name}/matched')
        prepare_dir(f'{src_dir}/checker/{chunk_name}/none')
        prepare_dir(f'{src_dir}/checker/{chunk_name}/repair')
        prepare_dir(f'{src_dir}/checker/{chunk_name}/final')

        print(chunk_name)
        read_video(chunk_name)
