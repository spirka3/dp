import cv2
import os
import supervision as sv

from ultralytics import YOLO

MODEL_PATH = "/home/s/spirka3/v8/weights/nm9_best.pt"

model = YOLO(MODEL_PATH)

box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=1,
    text_scale=0.5
)

for ride in ['1']:
# for ride in ['6', '7', '8']:
# for ride in ['3', '4', '5']:

    os.makedirs(f"results_new/{ride}", exist_ok=True)
    # os.makedirs(f"results_new/{ride}/images", exist_ok=True)
    # os.makedirs(f"results_new/{ride}/labels", exist_ok=True)

    SOURCE_VIDEO_PATH = f"videos/scenevideo-{ride}.mp4"
    # OUTPUT_IMAGE_PATH = f"results_new/{ride}/images"
    # OUTPUT_LABEL_PATH = f"results_new/{ride}/labels"
    OUTPUT_VIDEO_PATH = f"results_new/{ride}/scenevideo.mp4"

    frame_id = 0

    vf = open(f"results_new/{ride}/labels.txt", "w")

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    output = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, 25.0, (1920, 1080))

    for result in model.track(source=SOURCE_VIDEO_PATH, conf=0.2, stream=True, agnostic_nms=True, device=1):

        frame = result.orig_img

        detections = sv.Detections.from_yolov8(result)

        if len(detections) == 0:
            frame_id += 1
            output.write(frame)
            continue

        if result.boxes.obj is not None:
            detections.tracker_id = result.boxes.obj.cpu().numpy().astype(int)

        labels = [
            f"#{tracker_id} {confidence:0.2f}"
            for _, confidence, class_id, tracker_id
            in detections
        ]

        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )

        output.write(frame)

        # cv2.imwrite(f"{OUTPUT_IMAGE_PATH}/{frame_id}.jpg", frame)

        confs = [confidence for _, confidence, class_id, tracker_id in detections]
        tracs = [tracker_id for _, confidence, class_id, tracker_id in detections]

        # with open(f'{OUTPUT_LABEL_PATH}/{frame_id}.txt', "w") as f:
        # write data to file
        for i, xyxy in enumerate(detections.xyxy):
            x1, y1, x2, y2 = xyxy
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            w = x2 - x1
            h = y2 - y1
            x = float("{:.6f}".format(x/1920))
            y = float("{:.6f}".format(y/1080))
            w = float("{:.6f}".format(w/1920))
            h = float("{:.6f}".format(h/1080))
            # f.write(f"ad {x} {y} {w} {h}\n")
            vf.write(f"{frame_id} Ad {tracs[i]} {int(x1)} {int(y1)} {int(x2)} {int(y2)} {confs[i]:0.2f}\n")

        frame_id += 1

    vf.close()
    output.release()
