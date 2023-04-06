import cv2
import os

from utils import draw_text

DRIVER = 6
RED = (128, 0, 255)
BLUE = (255, 128, 0)
GREEN = (50, 205, 50)
ORANGE = (0, 165, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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


def find_fixations(frame_id, frame_bb):
    fixation = []
    id, cls, x1, y1, x2, y2, conf = frame_bb
    box2 = (x1, y1, x2, y2)

    for j in range(2):
        gaze, color = gazes[frame_id][j]
        x, y = gaze

        x1 = x - 40
        y1 = y - 40
        x2 = x + 40
        y2 = y + 40

        box1 = (x1, y1, x2, y2)

        # check if gaze is in object box
        if calc_iou(box1, box2) > 0.05:
            fixation.append(gaze)

    return fixation


def get_gazes():
    count = 0
    _gazes = dict()
    prev2_gaze = [1920/2, 1080/2]
    prev1_gaze = [1920/2, 1080/2]
    with open(f'{DRIVER}/gazedata', 'r') as f:
        lines = f.readlines()
        frame = -1
        for i, line in enumerate(lines):
            # save two of the gaze points for each frame
            if i % 2 == 0:
                frame += 1
                _gazes[frame] = []

            # eval text to json object
            json_gaze = eval(line)

            try:
                # get gaze data
                gaze = json_gaze['data']['gaze2d']
                color = BLUE
                count = 0
            except:
                if count < 2:
                    # if gaze data is not available, compute gaze points
                    direction = 1
                    if prev2_gaze[0] > prev1_gaze[0]:
                        direction = -1
                    gaze = [prev1_gaze[0] + direction * (prev1_gaze[0] - prev2_gaze[0]),
                            prev1_gaze[1] + direction * (prev1_gaze[1] - prev2_gaze[1])]
                    color = RED
                    count += 1
                else:
                    x, y = 0.5, 0.6
                    gaze = [x, y]
                    color = WHITE

            prev2_gaze = prev1_gaze
            prev1_gaze = gaze

            # add to list
            x, y = gaze
            x = int(x * 1920)
            y = int(y * 1080)

            if x > 1920 or y > 1080 or x < 0 or y < 0:
                x, y = int(1920/2), int(0.6 * 1080)
                color = WHITE

            _gazes[frame].append(((x, y), color))

    return _gazes


def process_labels():
    _labels = dict()
    _boxes = dict()
    with open(f'{DRIVER}/labels.txt', 'r') as f:
        for line in f.readlines():
            frame_id, cls, object_id, x1, y1, x2, y2, conf = line.strip().split(' ')

            frame_id = int(frame_id)
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            conf = conf[:4]

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

            if frame_id not in _labels.keys():
                _labels[frame_id] = []
                _boxes[frame_id] = []
            _labels[frame_id].append((cls, x, y, w, h))
            _boxes[frame_id].append((frame_id, cls, x1, y1, x2, y2, conf))

    return _labels, _boxes


def process_frames(object_id, start_frame, end_frame):
    global counter, last_labeled_frame  #, labels, gazes, boxes

    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    os.makedirs(f'{DRIVER}/OBJECTS/{object_id}', exist_ok=True)
    # os.makedirs(f'{DRIVER}/objects/{object_id}/labels', exist_ok=True)
    # os.makedirs(f'{DRIVER}/seen/{object_id}', exist_ok=True)

    t = end_frame - start_frame + 1
    for i in range(end_frame - start_frame + 1):
        ret, frame = video.read()
        frame_id = start_frame + i

        if gazes[frame_id][0][1] == WHITE and gazes[frame_id][1][1] == WHITE:
            t -= 1
            continue

        counter += 1

        labeled_frame = frame_id

        # if frame_id not in labels.keys():
        #     if last_labeled_frame != 0:
        #         labeled_frame = last_labeled_frame
        #     else:
        #         continue

        border = 2

        fixation_gazes = []

        # if frame_id in labels.keys():
        #     with open(f'{DRIVER}/labels/{object_id}_{frame_id}_{t}.txt', 'w') as f:
        #         frame_bbs = boxes[labeled_frame]
        #         for j, label in enumerate(labels[labeled_frame]):
        #             cls, x, y, w, h = label
        #             f.write(f'{object_id} {x} {y} {w} {h}\n')
        #
        #             frame_bb = frame_bbs[j]
        #             id, cls, x1, y1, x2, y2, conf = frame_bb
        #             fixations = find_fixations(frame_id, frame_bb)
        #
        #             color = ORANGE
        #             if len(fixations) > 0:
        #                 for fixation in fixations:
        #                     fixation_gazes.append(fixation)
        #                 color = GREEN
        #
        #             cv2.rectangle(frame, (x1, y1), (x2, y2), color, border)
        #             draw_text(frame, f'#{id} {cls} {conf}', pos=(x1 - border, y1), text_color_bg=color, padding=border)

        # draw both gaze points
        for k in range(2):
            gaze, color = gazes[frame_id][k]
            inner_color = color

            if color == WHITE:
                continue

            x, y = gaze
            if (x, y) in fixation_gazes:
                color = GREEN

            cv2.circle(frame, (x, y), 40, color, border)
            cv2.circle(frame, (x, y), 20, inner_color, 1)

        # if len(fixation_gazes) > 0:
        #     cv2.imwrite(f'{DRIVER}/seen/{object_id}_{frame_id}_{t}.jpg', frame)
        # cv2.imwrite(f'{DRIVER}/images/{object_id}_{frame_id}_{t}.jpg', frame)
        cv2.imwrite(f'{DRIVER}/OBJECTS/{object_id}/{object_id}_{DRIVER}_{frame_id}.jpg', frame)

        last_labeled_frame = labeled_frame
        t -= 1


def main():
    with open(f'{DRIVER}/frames.txt', 'r') as f:
        for object_id, line in enumerate(f.readlines()):
            prev_counter = counter
            _, start_frame, end_frame = line.strip().split(' ')
            process_frames(object_id, int(start_frame), int(end_frame))
            print(f'object {object_id} has {counter - prev_counter} frames')
    print('total frames:', counter)


if __name__ == "__main__":
    # every frame should have labels (and bounding boxes), bcs we specified the start and end frame of the object
    # if there is no label for a frame, we use the last labeled frame
    # if there is no label for the first frame, we skip the object
    # every frame has two gaze points, so we use both of them
    # we calculate the iou between the gaze points and the bounding boxes
    # if there is an iou, we draw the bounding box in green, otherwise in red
    # we are saving the frames into folder and creating the labels for each frame
    # seen frames are saved in a separate folder

    counter = 0
    last_labeled_frame = 0

    video = cv2.VideoCapture(f'{DRIVER}/scenevideo-{DRIVER}.mp4')
    os.makedirs(f'{DRIVER}/OBJECTS', exist_ok=True)
    # os.makedirs(f'{DRIVER}/images', exist_ok=True)
    # os.makedirs(f'{DRIVER}/labels', exist_ok=True)
    # os.makedirs(f'{DRIVER}/seen', exist_ok=True)

    # labels, boxes = process_labels()
    gazes = get_gazes()

    main()
