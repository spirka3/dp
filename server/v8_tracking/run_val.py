import subprocess
import torch

# check if device 1 is using
torch.cuda.set_device(1)
print(torch.cuda.utilization(device=None))

WEIGHTS = '/home/s/spirka3/v8/weights/nm10_best.pt'
METHOD = 'strongsort'

cmd = f'python val.py ' \
      f'--yolo-weights {WEIGHTS} ' \
      f'--tracking-method {METHOD} ' \
      f'--reid-weights osnet_ain_x1_0.pt ' \
      f'--split test ' \
      f'--benchmark MOTCUSTOM ' \
      f'--device 1 ' \

subprocess.run(cmd, shell=True)
