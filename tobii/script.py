# var = {
#     "type": "gaze", "timestamp": 0.010070,
#     "data": {
#         "gaze2d": [0.53915549670752083, 0.55159292431956286],
#         "gaze3d": [-82.44660708988151, -24.488478131606321, 895.6828387639049],
#         "eyeleft": {
#             "gazeorigin": [28.424467957380113, -10.880625489538037, -34.635359756659831],
#             "gazedirection": [-0.11825800788077551, -0.016374758108387139, 0.99284787901720484],
#             "pupildiameter": 4.6966419219970703
#         },
#         "eyeright": {
#             "gazeorigin": [-30.961429920829037, -9.551753993038524, -36.577715353971563],
#             "gazedirection": [-0.0552031586317921, -0.014137357542240984, 0.99837505297297768],
#             "pupildiameter": 4.7665619850158691
#         }
#     }
# }

import glob
import os

import cv2
from tqdm import tqdm

RIDE = '1'

PATH = f'/home/janci/Documents/DIPLO/PILOT/{RIDE} David Brandys'


def get_gazes():
    gazes = dict()
    prev2_gaze = [1920/2, 1080/2]
    prev1_gaze = [1920/2, 1080/2]
    with open(f'{PATH}/gazedata', 'r') as f:
        lines = f.readlines()
        frame = -1
        gazes[frame] = []
        for i, line in enumerate(lines):
            if i % 2 == 0:
                frame += 1
                gazes[frame] = []

            # text to json object
            json = eval(line)
            # get gaze data
            try:
                gaze = json['data']['gaze2d']
                color = (255, 128, 0)
            except:
                # if gaze data is not available, compute linear distance between last two gaze points
                gaze = [prev2_gaze[0] + (prev1_gaze[0] - prev2_gaze[0]) / 2,
                        prev2_gaze[1] + (prev1_gaze[1] - prev2_gaze[1]) / 2]
                color = (255, 128, 0)  # here we can use different color for interpolated gaze points

            prev2_gaze = prev1_gaze
            prev1_gaze = gaze

            # add to list
            gazes[frame].append([gaze, color])

    return gazes


def process_labels():
    frames = dict()  # frame_id: [[object_id, x, y, x, y, conf], [...]]
    objects = dict()  # object_id: [total frames, fixated frames, score]

    with open(f'{PATH}/labeled-video.txt', 'r') as f:
        labels = f.readlines()

        # reading the labels from file
        for label in tqdm(labels, desc=f"processing text file"):
            frame_id, cls, object_id, x1, y1, x2, y2, conf = label.strip().split(' ')

            if object_id == 'None':
                object_id = -1

            frame_id = int(frame_id)
            object_id = int(object_id)

            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            if frame_id not in frames.keys():
                frames[frame_id] = []
            frames[frame_id].append([object_id, x1, y1, x2, y2, conf])

            if object_id not in objects.keys():
                objects[object_id] = [0, 0, 0]
            objects[object_id][0] += 1

        print(f'Frames ({len(frames.keys())}): {frames}')
        print(f'Objects ({len(objects.keys())}): {objects}')

    return objects, frames


def calc_iou(box1, box2):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(box1[0], box2[0])
    yA = max(box1[1], box2[1])
    xB = min(box1[2], box2[2])
    yB = min(box1[3], box2[3])

    # compute the area of intersection rectangle
    inter_area = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if inter_area == 0:
        return 0

    # compute the area of both the prediction and ground-truth
    # rectangles
    box1_area = abs((box1[2] - box1[0]) * (box1[3] - box1[1]))
    box2_area = abs((box2[2] - box2[0]) * (box2[3] - box2[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the intersection area
    iou = inter_area / float(box1_area + box2_area - inter_area)

    # return the intersection over union value
    return iou


def find_iou(frame_id, gazes, frames):
    found_iou = False

    for j in range(2):
        x, y = gazes[frame_id + j][0]
        color = gazes[frame_id + j][1]

        cx = int(x * 1920)
        cy = int(y * 1080)
        x1 = cx - 40
        y1 = cy - 40
        x2 = cx + 40
        y2 = cy + 40

        box1 = (x1, y1, x2, y2)

        has_iou = []

        if frame_id in frames.keys():
            for data in frames[frame_id]:
                box2 = (data[1], data[2], data[3], data[4])
                # check if gaze is in object box
                iou = calc_iou(box1, box2)
                if iou > 0.05:
                    found_iou = True
                    has_iou.append(data)

        if found_iou:
            gaze = (cx, cy, color)
            return has_iou, gaze, frame_id + j

    x, y = gazes[frame_id + 1][0]
    color = gazes[frame_id + 1][1]

    cx = int(x * 1920)
    cy = int(y * 1080)

    return [], (cx, cy, color), frame_id + 1


def main():
    if not os.path.exists(f'{PATH}/iou'):
        os.makedirs(f'{PATH}/iou')

    # os remove files in folder
    for f in glob.glob(f'{PATH}/iou/*'):
        os.remove(f)

    gazes = get_gazes()
    objects, frames = process_labels()

    # reading the input
    cap = cv2.VideoCapture(f'{PATH}/scenevideo-{RIDE}.mp4')

    output = cv2.VideoWriter(
        f'{PATH}/gaze-video.avi', cv2.VideoWriter_fourcc(*'MPEG'),
        25, (1920, 1080))

    frame_id = 0

    while True:
        # if frame_id > 1000:
        #     break

        if frame_id % 500 == 0:
            print(frame_id)

        ret, frame = cap.read()

        if ret:
            # has_iou, gaze, oframe_id = find_iou(frame_id, gazes, frames)
            # cx, cy, color = gaze

            # draw object boxes
            # if oframe_id in frames.keys():
            if frame_id in frames.keys():
                for data in frames[frame_id]:
                    box2 = (data[1], data[2], data[3], data[4])
                    cv2.rectangle(frame, (box2[0], box2[1]), (box2[2], box2[3]), (0, 0, 255), 2)

                cv2.imwrite(f'{PATH}/detected/{frame_id}.jpg', frame)

            # if len(has_iou) > 0:
            #     # draw gaze circle
            #     cv2.circle(frame, (cx, cy), 40, (0, 204, 0), 2)
            #     # save iou frame
            #     cv2.imwrite(f'{PATH}/iou/{frame_id}.jpg', frame)
            #     # write iou to file
            #     for data in has_iou:
            #         object_id, x1, y1, x2, y2, conf = data
            #         # write coordinates to file
            #         with open(f'{PATH}/iou/{frame_id}.txt', 'a') as f:
            #             f.write(f'gaze: {cx} {cy}\n')
            #             f.write(f'object: {object_id} {x1} {y1} {x2} {y2}\n')
            # else:
            #     # draw gaze circle
            #     cv2.circle(frame, (cx, cy), 40, color, 2)

            output.write(frame)
            frame_id += 1
        else:
            break

    output.release()
    cap.release()


if __name__ == "__main__":
    main()
