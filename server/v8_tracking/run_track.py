import subprocess

WEIGHTS = '/home/s/spirka3/v8/weights/nm10_best.pt'
SOURCE = '/home/s/spirka3/yolov8_tracking/samples/parts-1/0.mp4'
METHOD = 'strongsort'

cmd = f'python track.py ' \
      f'--device 1 ' \
      f'--yolo-weights {WEIGHTS} ' \
      f'--source {SOURCE} ' \
      f'--tracking-method {METHOD} ' \
      f'--reid-weights osnet_ain_x1_0.pt ' \
      f'--save-vid ' \
      f'--save-trajectories ' \
      f'--save-txt'

subprocess.run(cmd, shell=True)
