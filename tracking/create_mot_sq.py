import os
import cv2

from tracking.utils import draw_label, prepare_dir

if __name__ == '__main__':
    ride = '1'
    # chunk = '3'
    src_dir = f'ride-1'

    # create list of unique chunk names
    chunk_names = [x.split('.')[0] for x in os.listdir(f'{src_dir}/tracker/tracks') if x.endswith('.txt')]

    # for chunk_name in ['chunks-1-0']:
    #     repair_frames = [x.split('.')[0] for x in os.listdir(f'checker/{chunk_name}/repair')]

    for chunk in [9]:

        chunk_name = f'chunks-1-{chunk}'
        # if chunk_name == 'chunks-1-0':
        #     continue

        # SINGLE_FRAME = True
        used_frames = []
        counter = 0
        saved_labels = []

        # read 0.txt a filter out the lines with no image in output folder
        with open(f'{src_dir}/tracker/tracks/{chunk_name}.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                frame, obj, left, top, width, height, conf, x, y, z = line.split()

                # if SINGLE_FRAME and frame in used_frames:
                #     continue

                if os.path.exists(f'{src_dir}/checker/{chunk_name}/matched/' + frame + '.jpg'):
                    counter += 1
                    used_frames.append(frame)
                    # print(frame, obj, left, top, width, height, conf, x, y, z)
                    saved_labels.append((frame, obj, left, top, width, height, conf, x, y, z))

        mapping = dict()
        # mapping['1'] = ['193']
        # mapping['0'] = ['196', '193', '198', '207', '195']
        mapping['*'] = ['0']

        corrected_labels = []

        # for repaired in os.listdir('/home/janci/Downloads/0'):
        for repaired in os.listdir('/home/janci/Downloads/1-10'):
            filename = repaired.split('.')[0]
            # if filename == 'darknet':
            if filename == 'darknet' or f'chunks-{ride}-{chunk}-' not in filename:
                continue
            frame_id = filename.split('-')[-1]
            # with open('/home/janci/Downloads/0/' + repaired, 'r') as f:
            with open('/home/janci/Downloads/1-10/' + repaired, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    obj, x, y, w, h = line.split()
                    x, y, w, h = int(float(x) * 1920), int(float(y) * 1080), int(float(w) * 1920), int(float(h) * 1080)
                    left, top = int(x - w/2), int(y - h/2)
                    label = [frame_id, obj, left, top, w, h, 1, 0, 0, 0]
                    label = [str(x) for x in label]
                    # print(frame_id, obj, left, top, w, h, 1, 0, 0, 0)
                    corrected_labels.append(label)

        # print(len(corrected_labels))
        # print(corrected_labels)
        # exit()

        # with open('MOTCUSTOM/test/MOTCUSTOM-01/gt/gt.txt', 'w') as f:
        for label in saved_labels:
            frame_num, obj, left, top, width, height, conf, x, y, z = label
            # if obj in mapping values:
            for key, values in mapping.items():
                if obj in values:
                    obj = key
            if '*' in mapping.keys():
                obj = mapping['*'][0]
            label = [frame_num, obj, left, top, width, height, conf, x, y, z]
            corrected_labels.append(label)
            # print(' '.join(label))
            # print(' '.join(label), file=f)

        # sort correct_labels by frame number
        corrected_labels = sorted(corrected_labels, key=lambda x: int(x[0]))
        # print(len(corrected_labels))
        # for c in corrected_labels:
            # print(c)

        for label in corrected_labels:
            if int(label[0]) >= 511:
                label[1] = '2'
            # if int(label[0]) >= 338 and label[1] == '1':
            #     label[1] = '3'

        # exit(0)

        # read video
        cap = cv2.VideoCapture(f'{src_dir}/origin-chunks/chunks-{ride}-{chunk}.mp4')
        i_dir = prepare_dir(f'MOTCUSTOM/test/MOTCUSTOM-0{chunk}/img1')
        g_dir = prepare_dir(f'MOTCUSTOM/test/MOTCUSTOM-0{chunk}/gt')
        f_dir = prepare_dir(f'{src_dir}/checker/chunks-{ride}-{chunk}/final')

        used_frames = []

        while True:

            ret, frame = cap.read()
            if not ret:
                break

            frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            frame_name = f'{str(frame_num).zfill(6)}.jpg'

            cv2.imwrite(f'{i_dir}/{frame_name}', frame)

            for label in corrected_labels:
                if label[0] == str(frame_num):
                    c, left, top, width, height, conf = label[1], int(label[2]), int(label[3]), int(label[4]), int(label[5]), label[6]
                    x1, y1, x2, y2 = left, top, left + width, top + height
                    label = (c, x1, y1, x2, y2, conf)

                    draw_label(frame, label, color=(12, 255, 25), border=2)
                    cv2.imwrite(f'{f_dir}/{frame_name}', frame)

                    if c != '0' and c != '1' and c not in used_frames:
                        used_frames.append(c)
                        cv2.imwrite(f'{f_dir}/__{frame_name}', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

        with open(f'{g_dir}/gt.txt', 'a') as f:
            for label in corrected_labels:
                print(' '.join(label), file=f)
