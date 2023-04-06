import os
import cv2


def read_video(chunk_name):
    repair_frames = [x.split('.')[0] for x in os.listdir(f'{src_dir}/checker/{chunk_name}/repair')]

    cap = cv2.VideoCapture(f'{src_dir}/origin-chunks/{chunk_name}.mp4')
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame_id = str(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))

        if frame_id in repair_frames:
            cv2.imwrite(f'{src_dir}/checker/{chunk_name}/images/{chunk_name}-{frame_id}.jpg', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    ride = '1'
    src_dir = f'ride-1'

    # create list of unique chunk names
    chunk_names = [x.split('.')[0] for x in os.listdir(f'{src_dir}/tracker/tracks')]


    for chunk_name in ['chunks-1-10']:
        if chunk_name == 'chunks-1-0':
            continue
        os.makedirs(f'{src_dir}/checker/{chunk_name}/images', exist_ok=True)
        read_video(chunk_name)
